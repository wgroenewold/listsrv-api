terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.48.0"
    }
  }
}

provider "openstack" {
  user_name   = "wouter"
  tenant_name = "admin"
  password    = "supers3cr3t"
  auth_url    = "hb-openstack.hpc.rug.nl:5000/v3"
  region      = "RegionOne"
}

variable external_network_name {
  default = "external"
}

variable keypair_name {
  default = "wouter"
}

variable private_network_name {
  default = "listsrv_mgmt_nt"
}

variable private_subnet_name {
  default = "listsrv_mgmt_sb"
} 

variable "router_name" {
  defadefault = "listsrv_mgmt_rt"  
}

variable "server_name" {
  default = "listsrv_mgmt"
}

variable "ssh_port"{
  default = 22
}

variable "subnet_cidr" {
  default = "10.0.0.0/24"
}

data "openstack_images_image_v2" "image" {
  name        = "RockyLinux-8.7"
  most_recent = true
}

data "openstack_compute_flavor_v2" "flavor" {
  name = "general.v1.small"
}

data "openstack_networking_network_v2" "external_network" {
  name = var.external_network_name
}

resource "openstack_networking_network_v2" "private_network" {
  name           =  var.private_network_name
  admin_state_up = true
}

resource "openstack_networking_subnet_v2" "private_subnet" {
  name       = var.private_subnet_name
  network_id = "${openstack_networking_network_v2.private_network.id}"
  cidr       = var.subnet_cidr
}

resource "openstack_networking_port_v2" "private_port" {
  network_id = "${openstack_networking_network_v2.private_network.id}"

  fixed_ip {
    subnet_id = "${openstack_networking_subnet_v2.private_subnet.id}"
  }
}

resource "openstack_networking_router_v2" "private_router" {
  name                = var.router_name
  external_network_id = "${openstack_networking_network_v2.external_network.id}"
  admin_state_up      = true
}

resource "openstack_networking_router_interface_v2" "private_interface" {
  router_id = "${openstack_networking_router_v2.private_router.id}"
  subnet_id = "${openstack_networking_subnet_v2.private_subnet.id}"
}


resource "openstack_networking_floatingip_v2" "fip_1"{
    pool  = data.openstack_networking_network_v2.external_network.name
}

resource "openstack_compute_secgroup_v2" "secgroup_1" {
  name        = "default"

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = -1
    to_port     = -1
    ip_protocol = "icmp"
    cidr        = "0.0.0.0/0"
  }

  # needed for exposure to outside of the API
  # rule {
  #   from_port   = 443
  #   to_port     = 443
  #   ip_protocol = "tcp"
  #   cidr        = "0.0.0.0/0"
  # }
}

resource "openstack_compute_instance_v2" "instance_1" {
  name            = var.server_name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair_name
  security_groups = ["${openstack_compute_secgroup_v2.secgroup_1.name}"]

  network {
    port = "${openstack_networking_port_v2.port_1.id}"
  }
}

resource "openstack_compute_floatingip_associate_v2" "fip_1" {
  floating_ip = "${openstack_compute_floatingip_v2.fip_1.address}"
  instance_id = "${openstack_compute_instance_v2.instance_1.id}"
}


output "serverip" {
 value = openstack_compute_instance_v2.instance_1.access_ip_v4
}