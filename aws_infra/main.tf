#######################################
# General configs
#######################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.2"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.profile

}

#######################################
# Compute module
#######################################

module "compute" {
  source                = "./modules/compute"
  key_name              = var.key_name
  subnet_ids            = module.vpc.public_subnet_ids
  sg_id                 = module.security.ec2_sg_id
  ami_id                = var.ami_id
  instance_type         = var.instance_type
  app_name              = var.app_name
  environment_name      = var.environment_name
  instance_profile_name = module.iam.ec2_instance_profile_name
  asg_min_size          = var.asg_min_size
  asg_max_size          = var.asg_max_size
  asg_desired_capacity  = var.asg_desired_capacity
  target_group_arn      = module.alb.alb_target_group_arn
}

#######################################
# Security module
#######################################
module "security" {
  source           = "./modules/security"
  vpc_id           = module.vpc.vpc_id
  app_name         = var.app_name
  environment_name = var.environment_name
  flask_port       = var.flask_port
  ssh_port         = var.ssh_port
  http_port        = var.http_port
  https_port       = var.https_port
  postgres_port    = var.postgres_port
  allowed_ssh_ip   = var.allowed_ssh_ip
}

#######################################
# VPC module
#######################################

module "vpc" {
  source               = "./modules/vpc"
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  app_name             = var.app_name
  environment_name     = var.environment_name
  availability_zones   = var.availability_zones
}

#######################################
# ALB module
#######################################

module "alb" {
  source            = "./modules/alb"
  app_name          = var.app_name
  environment_name  = var.environment_name
  alb_ports         = var.alb_ports
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  alb_sg_id         = module.security.alb_sg_id
}

#######################################
# Database module
#######################################

module "database" {
  source                 = "./modules/database"
  db_class               = var.db_class
  db_name                = var.db_name
  db_user                = var.db_user
  db_pass                = var.db_pass
  read_replica_az        = var.read_replica_az
  subnet_ids             = module.vpc.private_subnet_ids
  vpc_security_group_ids = [module.security.rds_sg_id]
}

#######################################
# Monitoring module
#######################################

module "monitoring" {
  source           = "./modules/monitoring"
  app_name         = var.app_name
  environment_name = var.environment_name
  asg_name         = module.compute.autoscaling_group_name
  cpu_threshold    = var.cpu_threshold
  disk_threshold   = var.disk_threshold
  alert_email      = var.alert_email
}

#######################################
# Storage module
#######################################

module "storage" {
  source          = "./modules/storage"
  bucket_prefix   = var.bucket_prefix
  ec2_s3_role_arn = module.iam.ec2_s3_role_arn
}

#######################################
# IAM module
#######################################

module "iam" {
  source           = "./modules/iam"
  app_name         = var.app_name
  environment_name = var.environment_name
  s3_bucket_arn    = module.storage.bucket_arn
}
