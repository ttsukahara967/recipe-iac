output "api_url" {
  description = "Base URL of the backend API (passed to the frontend as API_URL)"
  value       = "http://${aws_lb.api.dns_name}"
}

output "db_endpoint" {
  value = aws_rds_cluster.main.endpoint
}

output "ecs_cluster" {
  value = aws_ecs_cluster.main.name
}
