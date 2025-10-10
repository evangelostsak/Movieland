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
# IAM Variables
#######################################

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket EC2 should access"
  type        = string
}