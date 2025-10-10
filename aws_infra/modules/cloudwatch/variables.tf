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
# CloudWatch Variables
#######################################

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