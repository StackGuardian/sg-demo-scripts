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
