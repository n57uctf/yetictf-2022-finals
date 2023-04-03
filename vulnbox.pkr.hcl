packer {
  required_plugins {
    virtualbox = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/virtualbox"
    }
  }
}

# need to be autodetected before build as PKR_VAR_bridgeadapter or -var bridgeadapter
variable "bridgeadapter" { 
  type = string
  default = "eth0" 
}

variable "username" {
  type = string
}

variable "password" {
  type = string
}

variable "event" {
  type = string
}

variable "services" {
  type = list(string)
}


source "virtualbox-iso" "vulnbox" {
  vm_name = var.event
  nested_virt = true
  headless = true
  guest_os_type = "ArchLinux_64"
  iso_url = "https://mirror.yandex.ru/archlinux/iso/2023.03.01/archlinux-x86_64.iso"
  iso_checksum = "file:https://mirror.yandex.ru/archlinux/iso/2023.03.01/sha256sums.txt"
  ssh_username = var.username
  ssh_password = var.password
  memory = 4096
  cpus = 2
  shutdown_command = "echo '${var.password}' | sudo -S shutdown -P now"
  http_directory = ".packer"
  hard_drive_interface = "sata"
  boot_command = [
    "<wait1m>",
    "echo '{\"!users\": [{\"!password\": \"${var.password}\",\"sudo\": true,\"username\": \"${var.username}\"}]}' > user_credentials.json<enter><wait>",
    "curl -O 'http://{{.HTTPIP}}:{{.HTTPPort}}/user_{configuration,disk_layout}.json'<enter><wait>",
    "pacman -Sy<enter><wait>",
    "archinstall --creds user_credentials.json --config user_configuration.json --disk_layouts user_disk_layout.json --debug --silent<enter><wait10m>",
    "if [[ $? -eq 0 ]]; then arch-chroot /mnt/archinstall systemctl enable sshd && systemctl reboot; fi<enter><wait1m>",
  ]
  guest_additions_mode = "disable"
  disk_size = 15000
  vboxmanage_post = [
    ["modifyvm", "{{.Name}}", "--nic2", "bridged"],
    ["modifyvm", "{{.Name}}", "--bridgeadapter2", var.bridgeadapter],
    ["modifyvm", "{{.Name}}", "--macaddress2", "0274616e756b"],
    ["modifyvm", "{{.Name}}", "--cableconnected1", "off"]
  ]
  export_opts = [
    "--manifest",
    "--vsys", "0",
    "--description", "ssh ${var.username}@10.0.<N>.2\nPassword: ${var.password}"
  ]
  format = "ova"
}

build {
  sources = [
    "source.virtualbox-iso.vulnbox",
  ]
  provisioner "file"{
    sources = [for s in var.services: "./${s}/${lower(s)}"]
    destination = "/home/${var.username}/"
  }

  provisioner "shell" {
    inline = [
      "echo ${var.password} | sudo -S systemctl enable sshd",
      "echo ${var.password} | sudo -S systemctl enable docker",
      "echo ${var.password} | sudo -S systemctl start docker",
      "echo '${var.password}' | sudo -S usermod -aG docker ${var.username}"
    ]
  }
  provisioner "shell" {
    inline = [for s in var.services: "echo ${var.password} | sudo -S docker-compose -f ./${lower(s)}/docker-compose.yml up --quiet-pull -d"]
  }

  provisioner "shell"{
    inline = ["history -c"]
  }
}
