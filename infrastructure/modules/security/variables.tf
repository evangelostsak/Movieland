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

variable "security_group_ports" {
  description = "List of ports to open in the security group"
  type        = list(number)
}

variable "protocols" {
  description = "Protocols for the Application Load Balancer"
  type        = list(string)
}