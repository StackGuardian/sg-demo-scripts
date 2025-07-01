output "secret_value" {
  value     = var.secret_name != "" ? data.aws_secretsmanager_secret_version.this[0].secret_string : null
  sensitive = true
}

output "secrets" {
  value = var.secret_name != "" ? null : data.aws_secretsmanager_secrets.this[0].names
}
