variable "region" { type = string default = "us-east-1" }
variable "project_name" { type = string default = "ai-cost-optimizer" }
variable "report_prefix" { type = string default = "reports" }
variable "schedule_expression" { type = string default = "cron(0 12 * * ? *)" }
