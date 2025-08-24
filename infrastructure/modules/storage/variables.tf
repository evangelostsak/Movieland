# S3 Variables
variable "bucket_prefix" {
  description = "prefix of s3 bucket for app data"
  type        = string
}

variable "ec2_s3_role_arn" {
  type = string
  description = "ARN of the EC2 IAM role for S3 access"
}