import pulumi
import pulumi_aws as aws
import pulumi_tls as tls  # To generate a new key pair dynamically

# Variables
ami_id = "ami-03fd334507439f4d1"  # Use your desired AMI ID
instance_type = "t2.micro"         # EC2 instance type
region = "eu-west-1"               # AWS region
iilin_ssh_public_key = (
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOkAhvfRyUvgsUwENIds1a/4OvuHQgLki8K1EzPltl5M"
    " i.ilin@iilin-pro14.local"
)

# Generate an SSH Key Pair dynamically with Pulumi
ssh_key = tls.PrivateKey("ssh-key", algorithm="ED25519")  # Generate an ED25519 private key

# Create an AWS Key Pair with the generated public key
key_pair = aws.ec2.KeyPair("generated-key-pair", public_key=ssh_key.public_key_openssh)

# Define Security Group
server_sg = aws.ec2.SecurityGroup("ec2-security-group",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],  # SSH access from anywhere
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=5432,
            to_port=5435,
            self=True,  # Allow communication between instances in the same group
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",  # Allow all outbound traffic
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ]
)

# Create EC2 instance 3
server_3 = aws.ec2.Instance("server-3",
    ami=ami_id,
    instance_type=instance_type,
    key_name=key_pair.key_name,  # Attach AWS key pair
    vpc_security_group_ids=[server_sg.id],
    tags={"Name": "server-3"},
    user_data=f"""#!/bin/bash
        mkdir -p /home/ubuntu/.ssh
        echo '{iilin_ssh_public_key}' >> /home/ubuntu/.ssh/authorized_keys  # Add iilin ssh public key only
        chmod 700 /home/ubuntu/.ssh
        chmod 600 /home/ubuntu/.ssh/authorized_keys
        chown -R ubuntu:ubuntu /home/ubuntu/.ssh
    """
)

# Create EC2 instance 4
server_4 = aws.ec2.Instance("server-4",
    ami=ami_id,
    instance_type=instance_type,
    key_name=key_pair.key_name,  # Attach AWS key pair
    vpc_security_group_ids=[server_sg.id],
    tags={"Name": "server-4"},
    user_data=f"""#!/bin/bash
        mkdir -p /home/ubuntu/.ssh
        echo '{iilin_ssh_public_key}' >> /home/ubuntu/.ssh/authorized_keys  # Add iilin ssh public key only
        chmod 700 /home/ubuntu/.ssh
        chmod 600 /home/ubuntu/.ssh/authorized_keys
        chown -R ubuntu:ubuntu /home/ubuntu/.ssh
    """
)

# Outputs
pulumi.export("server_3_public_ip", server_3.public_ip)
pulumi.export("server_4_public_ip", server_4.public_ip)
pulumi.export("security_group_id", server_sg.id)
pulumi.export("generated_private_key", pulumi.Output.secret(ssh_key.private_key_pem))