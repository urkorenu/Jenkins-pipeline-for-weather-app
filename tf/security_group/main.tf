# Security Group for ALB
resource "aws_security_group" "allow_all_sg" {
  vpc_id = var.vpc_id

  # Rule to allow all inbound traffic (not recommended for production)
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security Group for Production Instance (restricted)
resource "aws_security_group" "production_sg" {
  vpc_id = var.vpc_id

  # Ingress rule to allow access from the ALB
  ingress {
    from_port   = 9000  # Production app is running on port 9000
    to_port     = 9000
    protocol    = "tcp"
    security_groups = [aws_security_group.allow_all_sg.id]
  }

  # Egress rule to allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}


