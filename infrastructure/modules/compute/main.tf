resource "aws_launch_template" "app_template" {
  name_prefix          = "${var.app_name}-${var.environment_name}-app"
  image_id             = var.ami_id
  instance_type        = var.instance_type
  key_name             = var.key_name
  iam_instance_profile {
    name = var.instance_profile_name
  }
  monitoring {
    enabled = true
  }
  vpc_security_group_ids = [var.sg_id]

  # Dynamically configure CloudWatch Agent using file
  user_data = file("${path.module}/cloudwatch.sh")
}

resource "aws_autoscaling_group" "app_asg" {
  name                      = "${var.app_name}-${var.environment_name}-asg"
  min_size                  = var.asg_min_size
  max_size                  = var.asg_max_size
  desired_capacity          = var.asg_desired_capacity
  vpc_zone_identifier       = var.subnet_ids
  target_group_arns         = [var.target_group_arn]
  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.app_template.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.app_name}-${var.environment_name}-instance"
    propagate_at_launch = true
  }
}