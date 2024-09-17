locals {
  name = "tf-jenkins"
}

data "aws_region" "current" {}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

module "aws_vpc" {
  source = "./vpc"
}

module "subnets" {
  source         = "./subnets"
  vpc_id         = module.aws_vpc.id
  int_gateway_id = module.aws_internet_gateway.int_gateway_id
  allow_all_sg   = module.aws_security_group.allow_all_id
}

module "aws_internet_gateway" {
  source = "./internet_gateway"
  vpc_id = module.aws_vpc.id
}

module "aws_security_group" {
  source = "./security_group"
  vpc_id = module.aws_vpc.id
}

# NAT instance 
module "fck-nat" {
  source = "RaJiska/fck-nat/aws"
  name      = local.name
  vpc_id    = module.aws_vpc.id
  subnet_id = module.subnets.public_a
  ha_mode   = true
  #use_ssh   = true
  #ssh_key_name = "ansible"
  update_route_table = true
  route_table_id     = module.subnets.private_rt
}

# Route for Private Subnet to Use NAT Instance
#resource "aws_route" "private_nat_route" {
#  route_table_id         = aws_route_table.private_rt.id
#  destination_cidr_block = "0.0.0.0/0"
#  #network_interface_id   = aws_instance.jenkins-nat-instance.primary_network_interface_id
#}

# GitLab EC2 Instance
#resource "aws_instance" "gitlab" {
# ami                    = data.aws_ami.ubuntu.id
#instance_type          = "t3.medium"
#subnet_id              = module.subnets.private
#vpc_security_group_ids = [module.aws_security_group.allow_all_id]
#key_name               = "ansible"
#tags = {
#  Name = "GitLab-Server"
#}
#}

# Jenkins Master EC2 Instance
#resource "aws_instance" "jenkins_master" {
#  ami                    = data.aws_ami.ubuntu.id
#  instance_type          = "t3.micro"
#  subnet_id              = module.subnets.private
#  vpc_security_group_ids = [module.aws_security_group.allow_all_id]
#  key_name               = "ansible"
#  tags = {
#    Name = "Jenkins-Master"
#  }
#}

# Jenkins Agent EC2 Instance
#resource "aws_instance" "jenkins_agent" {
#  ami                    = data.aws_ami.ubuntu.id
#  instance_type          = "t3.micro"
#  subnet_id              = module.subnets.private
#  vpc_security_group_ids = [module.aws_security_group.allow_all_id]
# key_name               = "ansible"
# tags = {
#   Name = "Jenkins-Agent"
# }
#}

# Production EC2 Instance
resource "aws_instance" "production" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = module.subnets.private
  vpc_security_group_ids = [module.aws_security_group.prod_id]
  key_name               = "ansible"
  tags = {
    Name = "Production-Instance"
  }
}

# module "aws_lb" {
#  source           = "../lb"
#  vpc_id           = module.aws_vpc.id
#  public_sub_a     = module.subnets.public_a
#  public_sub_b     = module.subnets.public_b
#  allow_all_sg     = module.aws_security_group.allow_all_id
#  prod_instance_id = aws_instance.production.id
#}
