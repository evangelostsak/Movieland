
variable "app_name" {
  description = "Name of the web application"
  type        = string
}

variable "environment_name" {
  description = "Deployment environment (dev/staging/production)"
  type        = string
}

  variable "allowed_ssh_ip" {
  description = "IP address to allow SSH access"
  type        = string
}

# VPC & Subnet CIDRs

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "List of CIDRs for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  description = "List of CIDRs for private subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones to deploy into"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}