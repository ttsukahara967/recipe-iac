# Optional custom domain. With domain_name = "" everything stays on the default AWS hostnames
# and the API is served over plain HTTP.
#
#   production: ouchirecipes.com          (site)   api.ouchirecipes.com          (API)
#   develop:    develop.ouchirecipes.com  (site)   api.develop.ouchirecipes.com  (API)
#
# The hosted zone is created by the Route 53 domain registration and is not managed here.
# The site's certificate and DNS records are created by SST (frontend/sst.config.ts).

locals {
  use_domain  = var.domain_name != ""
  site_domain = !local.use_domain ? "" : (var.environment == "production" ? var.domain_name : "${var.environment}.${var.domain_name}")
  api_domain  = local.use_domain ? "api.${local.site_domain}" : ""
}

data "aws_route53_zone" "main" {
  count = local.use_domain ? 1 : 0
  name  = var.domain_name
}

resource "aws_acm_certificate" "api" {
  count             = local.use_domain ? 1 : 0
  domain_name       = local.api_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "api_cert_validation" {
  for_each = {
    for o in flatten(aws_acm_certificate.api[*].domain_validation_options) : o.domain_name => o
  }

  zone_id         = data.aws_route53_zone.main[0].zone_id
  name            = each.value.resource_record_name
  type            = each.value.resource_record_type
  records         = [each.value.resource_record_value]
  ttl             = 60
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "api" {
  count                   = local.use_domain ? 1 : 0
  certificate_arn         = aws_acm_certificate.api[0].arn
  validation_record_fqdns = [for r in aws_route53_record.api_cert_validation : r.fqdn]
}

resource "aws_route53_record" "api" {
  count   = local.use_domain ? 1 : 0
  zone_id = data.aws_route53_zone.main[0].zone_id
  name    = local.api_domain
  type    = "A"

  alias {
    name                   = aws_lb.api.dns_name
    zone_id                = aws_lb.api.zone_id
    evaluate_target_health = false
  }
}
