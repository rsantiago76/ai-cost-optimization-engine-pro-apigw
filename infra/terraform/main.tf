terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.0" }
  }
}

provider "aws" { region = var.region }

resource "aws_s3_bucket" "reports" { bucket_prefix = "${var.project_name}-reports-" }

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../"
  output_path = "${path.module}/lambda_bundle.zip"
  excludes    = [
    "infra/terraform/.terraform",
    "infra/terraform/*.tfstate*",
    "dashboard/node_modules",
    ".git",
    "**/__pycache__",
    "out",
    "*.zip"
  ]
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_least_priv" {
  name   = "${var.project_name}-least-priv"
  policy = templatefile("${path.module}/policy.tpl.json", {
    bucket_arn   = aws_s3_bucket.reports.arn,
    prefix       = var.report_prefix
  })
}

resource "aws_iam_role_policy_attachment" "attach_custom" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_least_priv.arn
}

resource "aws_iam_role_policy_attachment" "attach_basic_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "cost_scan" {
  function_name = "${var.project_name}-daily-scan"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda.handler"
  runtime       = "python3.11"
  filename      = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout       = 60
  memory_size   = 512

  environment {
    variables = {
      REPORT_BUCKET = aws_s3_bucket.reports.bucket
      REPORT_PREFIX = var.report_prefix
    }
  }
}

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.project_name}-schedule"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "target" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "lambda"
  arn       = aws_lambda_function.cost_scan.arn
}

resource "aws_lambda_permission" "allow_events" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_scan.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}

output "report_bucket_name" { value = aws_s3_bucket.reports.bucket }
output "report_prefix" { value = var.report_prefix }


# ---------------- API Gateway (HTTP API) ----------------
resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.project_name}-http-api"
  protocol_type = "HTTP"
  cors_configuration {
    allow_headers = ["content-type", "authorization"]
    allow_methods = ["GET", "OPTIONS"]
    allow_origins = ["*"]
  }
}

resource "aws_lambda_function" "report_api" {
  function_name = "${var.project_name}-report-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "api_lambda.handler"
  runtime       = "python3.11"
  filename      = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout       = 30
  memory_size   = 512

  environment {
    variables = {
      REPORT_BUCKET = aws_s3_bucket.reports.bucket
      REPORT_PREFIX = var.report_prefix
      CORS_ORIGIN   = "*"
    }
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.report_api.arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "report_route" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "GET /report"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.report_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

output "api_base_url" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}
