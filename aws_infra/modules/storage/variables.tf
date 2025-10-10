#######################################
# Common Variables
#######################################
variable "project_name" {
  description = "Name of the Project"
  type        = string
}

variable "environment" {
  description = "Name of the Environment"
  type        = string
}

variable "common_tags" {
  description = "Common tags to be applied to all resources"
  type        = map(string)
  default     = {}
}

#######################################
# Storage Variables
#######################################

variable "bucket_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
}

variable "ec2_s3_role_arn" {
  type = string
  description = "ARN of the EC2 IAM role for S3 access"
}