locals {
  name     = "tf-jenkins"
}

# Public subnets (two different AZs)
resource "aws_subnet" "public_a" {
  vpc_id                    = var.vpc_id
  cidr_block                = "10.0.1.0/24"  # First public subnet
  availability_zone         = "eu-north-1a"  
  map_public_ip_on_launch   = true
  tags = {
    Name = "${local.name}-public"
  }
}

# Public route table
resource "aws_route_table" "public_rt" {
  vpc_id = var.vpc_id
  tags = {
    Name = "jenkins-rt-public1"
  }
}

resource "aws_route" "public_igw" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = var.int_gateway_id

}

# Associate public route table with public subnets
resource "aws_route_table_association" "public_association_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public_rt.id
}

# Private subnet
resource "aws_subnet" "private" {
  vpc_id            = var.vpc_id
  availability_zone = "eu-north-1a"
  cidr_block                = "10.0.2.0/24"  # First public subnet
  
  tags = {
    Name = "${local.name}-private"
  }
}

resource "aws_route_table" "private" {
  vpc_id = var.vpc_id

  tags = {
    Name = "${local.name}-private"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}