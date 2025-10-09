variable "bucket_prefix" {
  description = "prefix of s3 bucket for app data"
  type        = string
}

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/production)"
  type        = string
}

variable "common_tags" {
  description = "Common tags to be applied to all resources"
  type        = map(string)
  default     = {}
}

variable "ec2_s3_role_arn" {
  type = string
  description = "ARN of the EC2 IAM role for S3 access"
}