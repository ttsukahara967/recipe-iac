output "api_url" {
  description = "Base URL of the backend API (passed to the frontend as API_URL)"
  value       = local.use_domain ? "https://${local.api_domain}" : "http://${aws_lb.api.dns_name}"
}

output "db_endpoint" {
  value = aws_rds_cluster.main.endpoint
}

output "ecs_cluster" {
  value = aws_ecs_cluster.main.name
}

output "site_domain" {
  description = "Custom domain for the site (passed to SST as SITE_DOMAIN); empty when no domain is configured"
  value       = local.site_domain
}
