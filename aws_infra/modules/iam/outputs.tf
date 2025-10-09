output "ec2_instance_profile_name" {
  value = aws_iam_instance_profile.ec2_instance_profile.name
}

output "ec2_s3_role_arn" {
  value = aws_iam_role.ec2_s3_role.arn
}