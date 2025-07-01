variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "eu-central-1"
}

variable "secret_name" {
  description = "The name of the AWS Secrets Manager secret"
  type        = string
  default     = "terraform/SG/test-secret"
}

provider "aws" {
  region = var.region
}

data "aws_secretsmanager_secret" "this" {
  name = var.secret_name
}

data "aws_secretsmanager_secret_version" "this" {
  secret_id     = data.aws_secretsmanager_secret.this.id
  version_stage = "AWSCURRENT"
}

output "secret_value" {
  value     = data.aws_secretsmanager_secret_version.this.secret_string
  sensitive = true
}
