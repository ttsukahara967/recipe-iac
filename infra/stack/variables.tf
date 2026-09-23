variable "project" {
  type    = string
  default = "recipe-iac"
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["develop", "staging", "production"], var.environment)
    error_message = "environment must be one of develop / staging / production."
  }
}

variable "aws_region" {
  type    = string
  default = "ap-northeast-1"
}

variable "vpc_cidr" {
  type = string
}

variable "db_engine_version" {
  type    = string
  default = "17.10"
}

# Aurora Serverless v2 capacity (ACU). min=0 auto-pauses when idle, stopping compute charges
variable "db_min_acu" {
  type    = number
  default = 0
}

variable "db_max_acu" {
  type    = number
  default = 1
}

variable "db_auto_pause_seconds" {
  type    = number
  default = 300
}

# API image in ECR (the Makefile passes <repo>:<source hash>)
variable "api_image" {
  type    = string
  default = ""
}

# Fargate task size. 0.25 vCPU / 0.5 GB is the minimum
variable "api_cpu" {
  type    = number
  default = 256
}

variable "api_memory" {
  type    = number
  default = 512
}

variable "api_desired_count" {
  type    = number
  default = 1
}

variable "log_retention_days" {
  type    = number
  default = 7
}
