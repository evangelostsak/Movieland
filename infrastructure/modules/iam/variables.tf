variable "app_name" {
  type = string
}

variable "environment_name" {
  type = string
}

variable "s3_bucket_arn" {
  type = string
  description = "ARN of the S3 bucket EC2 should access"
}