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
# VPC Variables
#######################################

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "List of CIDRs for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "List of CIDRs for private subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones to deploy into"
  type        = list(string)
}