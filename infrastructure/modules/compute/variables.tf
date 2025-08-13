variable "key_name" {
  type        = string
  description = "Name of the SSH key pair to use for EC2 instances"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet ID for EC2 instance or ASG"
}

variable "sg_id" {
  type        = string
  description = "Security Group ID for EC2 instances"
}

variable "ami_id" {
  type        = string
  description = "AMI ID for the EC2 instance"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
}

variable "app_name" {
  type        = string
  description = "Application name tag"
}

variable "environment_name" {
  type        = string
  description = "Environment name tag"
}

variable "asg_min_size" {
  type        = number
  description = "Minimum number of instances in the ASG"
}

variable "asg_max_size" {
  type        = number
  description = "Maximum number of instances in the ASG"
}

variable "asg_desired_capacity" {
  type        = number
  description = "Desired capacity of the ASG"
}