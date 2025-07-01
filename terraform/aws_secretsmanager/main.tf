data "aws_secretsmanager_secret" "this" {
  count = var.secret_name != "" ? 1 : 0

  name = var.secret_name
}

data "aws_secretsmanager_secret_version" "this" {
  count = var.secret_name != "" ? 1 : 0

  secret_id     = data.aws_secretsmanager_secret.this[0].id
  version_stage = "AWSCURRENT"
}

data "aws_secretsmanager_secrets" "this" {
  count = var.secret_name != "" ? 0 : 1
}
