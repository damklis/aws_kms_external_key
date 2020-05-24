output "external_key_policy_name" {
  value = aws_iam_policy.external_key_policy.name
}

output "external_key_policy_arn" {
  value = aws_iam_policy.external_key_policy.arn
}

output "external_key_arn" {
  value = aws_kms_external_key.external_key.arn
}
