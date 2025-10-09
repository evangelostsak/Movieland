#######################################
# Common Variables
#######################################

variable "app_name" {
  description = "Name of the web application"
  type        = string
  default     = "web-app"
}

variable "environment_name" {
  description = "Deployment environment (dev/staging/production)"
  type        = string
  default     = "dev"
}

variable "profile" {
    description = "AWS profile to use for authentication"
    type        = string
}

variable "region" {
  description = "AWS region to deploy resources"
  type        = string
}

#######################################
# Compute module Variables
#######################################

variable "ami_id" {
  description = "Amazon machine image to use for ec2 instance"
  type        = string
}

variable "instance_type" {
  description = "ec2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of the key pair to use for ec2 instance"
  type        = string
}

variable "allowed_ssh_ip" {
  description = "IP address to allow SSH access"
  type        = string
}

variable "asg_min_size" {
  description = "Minimum number of instances in Auto Scaling Group"
  type        = number
}

variable "asg_max_size" {
  description = "Maximum number of instances in Auto Scaling Group"
  type        = number
}

variable "asg_desired_capacity" {
  description = "Desired number of instances in Auto Scaling Group"
  type        = number
}

#######################################
# Security module Variables
#######################################

variable "http_port" {
  description = "Port for HTTP traffic"
  type        = number
  default     = 80
}

variable "https_port" {
  description = "Port for HTTPS traffic"
  type        = number
  default     = 443
}

variable "postgres_port" {
  description = "Port for PostgreSQL traffic"
  type        = number
  default     = 5432
}

variable "flask_port" {
  description = "Port Flask app listens on"
  type        = number
}

variable "ssh_port" {
  description = "Port for SSH access"
  type        = number
  default     = 22
}

#######################################
# VPC module Variables
#######################################

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
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

#######################################
# ALB module Variables
#######################################

variable "alb_ports" {
  description = "Ports of the Application Load Balancer"
  type        = list(number)
}

#######################################
# Database module Variables
#######################################

variable "db_name" {
  description = "Name of DB"
  type        = string
}

variable "db_class" {
  description = "DB instance class"
  type        = string
}

variable "db_user" {
  description = "Username for DB"
  type        = string
}

variable "db_pass" {
  description = "Password for DB"
  type        = string
  sensitive   = true
}

variable "read_replica_az" {
  description = "Availability zone for read replica"
  type        = string
}

#######################################
# Monitoring module Variables
#######################################

variable "alert_email" {
  description = "Email address to receive CloudWatch alerts"
  type        = string
}

variable "cpu_threshold" {
  description = "CPU usage threshold for high CPU alarm"
  type        = number
  default     = 85
}

variable "disk_threshold" {
  description = "Disk usage threshold for low disk space alarm"
  type        = number
  default     = 75
}

#######################################
# Storage module Variables
#######################################

variable "bucket_prefix" {
  description = "prefix of s3 bucket for app data"
  type        = string
}

#######################################
# IAM module Variables
#######################################