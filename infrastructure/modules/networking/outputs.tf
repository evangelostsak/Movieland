output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.load_balancer.dns_name
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id,
    aws_subnet.public_c.id
  ]
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id,
    aws_subnet.private_c.id
  ]
}

output "alb_sg_id" {
  description = "Security Group ID for the ALB"
  value       = aws_security_group.alb.id
}

output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = aws_lb_target_group.instances.arn
}