# EC2 Variables

variable "ami" {
  description = "Amazon machine image to use for ec2 instance"
  type        = string
}

variable "instance_type" {
  description = "ec2 instance type"
  type        = string
}

variable "key_name" {
  description = "Name of the key pair to use for ec2 instance"
  type        = string
}

# ASG Variables

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