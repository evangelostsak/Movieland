
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
}

variable "private_subnet_cidrs" {
  description = "List of CIDRs for private subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "List of availability zones to deploy into"
  type        = list(string)
}

variable "alb_ports" {
  description = "Ports of the Application Load Balancer"
  type        = list(number)
}

variable "protocols" {
  description = "Protocols for the Application Load Balancer"
  type        = list(string)
}