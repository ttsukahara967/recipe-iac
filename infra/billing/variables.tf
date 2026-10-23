variable "aws_region" {
  type    = string
  default = "ap-northeast-1"
}

variable "project" {
  type    = string
  default = "recipe-iac"
}

variable "budget_alert_email" {
  type        = string
  description = "Email address that receives budget alerts and the daily cost report. Pass via TF_VAR_budget_alert_email; never commit it."
}

variable "budget_limit_usd" {
  type        = number
  default     = 100
  description = "Monthly budget in USD. Alerts fire at 80% (forecast), 100% and 150% (actual)."
}

variable "daily_report_cron_utc" {
  type        = string
  default     = "cron(0 22 * * ? *)" # 22:00 UTC = 07:00 JST
  description = "EventBridge schedule for the daily cost report."
}
