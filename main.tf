locals {
  external_key_description = "${var.key_alias}: external key for encryption"
}

provider "aws" {
  version = "~> 2.0"
  region  = var.region
}

resource "aws_kms_external_key" "external_key" {
  description = local.external_key_description
  tags        = var.tags
}

resource "aws_kms_alias" "external_key_alias" {
  name          = var.key_alias
  target_key_id = aws_kms_external_key.external_key.id
}

resource "null_resource" "import_key_material" {
  triggers = {
    external_key_exists = aws_kms_external_key.external_key.arn
  }

  provisioner "local-exec" {
    command     = "${path.module}/import_key_material.sh $key_id $algorithm"
    environment = {
      key_id     = aws_kms_external_key.external_key.id
      algorithm  = var.algorithm
    }
  }
}

data "aws_iam_policy_document" "external_key_policy_document" {
  statement {
    sid = "KMSExternalKeyFullAccess"
    actions = [
      "kms:*",
    ]
    resources = [
      aws_kms_external_key.external_key.arn
    ]
  }
}

resource "aws_iam_policy" "external_key_policy" {
  name        = var.policy_name
  path        = "/"
  policy      = data.aws_iam_policy_document.external_key_policy_document.json
}
