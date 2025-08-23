# Monitoring Variables

variable "alert_email" {
  description = "Email address for SNS alerts"
  type        = string
}
variable "asg_name" {
  description = "Name of the Auto Scaling Group to monitor"
  type        = string
}

variable "cpu_threshold" {
  description = "CPU usage threshold for high CPU alarm"
  type        = number
}

variable "disk_threshold" {
  description = "Disk usage threshold for low disk space alarm"
  type        = number
}

variable "app_name" {
  description = "Application name"
  type        = string
}

variable "environment_name" {
  description = "Environment name"
  type        = string
}