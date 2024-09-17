# Load Balancer Configuration
resource "aws_lb" "app_lb" {
  name               = "app-lb"
  internal           = false  # This is a public ALB
  load_balancer_type = "application"
  security_groups    = [var.allow_all_sg]
  subnets            = [var.public_sub_a, var.public_sub_b]
}

# Target Group for Production EC2 Instance
resource "aws_lb_target_group" "production_tg" {
  name     = "production-tg"
  port     = 9000  # Application is running on this port
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

# ALB Listener
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.production_tg.arn
  }
}

# Production Instance Target Group Attachment
resource "aws_lb_target_group_attachment" "prod_attachment" {
  target_group_arn = aws_lb_target_group.production_tg.arn
  target_id        = var.prod_instance_id
  port             = 9000  # Production instance is listening on port 9000
}

