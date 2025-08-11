# RDS Variables

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