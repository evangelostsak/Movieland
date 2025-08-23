
variable "app_name" {
  description = "Name of the web application"
  type        = string
}

variable "environment_name" {
  description = "Deployment environment (dev/staging/production)"
  type        = string
}

variable "alb_sg_id" {
  type        = string
  description = "Security group ID for the ALB"
}

variable "alb_ports" {
  description = "Ports of the Application Load Balancer"
  type        = list(number)
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}
