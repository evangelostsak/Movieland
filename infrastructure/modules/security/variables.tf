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
