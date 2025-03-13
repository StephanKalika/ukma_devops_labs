import pulumi
import pulumi_aws as aws
import pulumi_tls as tls  # To generate a new key pair dynamically

# Variables
ami_id = "ami-03fd334507439f4d1"  # Use your desired AMI ID
instance_type = "t2.micro"         # EC2 instance type
region = "eu-west-1"               # AWS region

# Generate an SSH Key Pair dynamically in Pulumi
private_key = tls.PrivateKey("ssh-key",
    algorithm="ED25519"  # Generate an ED25519 key pair
)

# Create an AWS Key Pair with the generated public key
key_pair = aws.ec2.KeyPair("my-key-pair",
    public_key=private_key.public_key_openssh  # Use OpenSSH format public key
)

# Define Security Group
server_sg = aws.ec2.SecurityGroup("server-sg",
    description="Allow authorized access to servers",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],  # Allow SSH access from anywhere
        ),
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

# Add rule to allow internal communication between instances
db_intraserver = aws.ec2.SecurityGroupRule("db-intraserver-rule",
    type="ingress",
    security_group_id=server_sg.id,
    from_port=5432,
    to_port=5435,
    protocol="tcp",
    source_security_group_id=server_sg.id,  # Internal communication
)

# Create EC2 instance 3
server_3 = aws.ec2.Instance("server-3",
    ami=ami_id,
    instance_type=instance_type,
    key_name=key_pair.key_name,
    security_groups=[server_sg.name],
    tags={"Name": "server-3"},
    user_data=f"""#!/bin/bash
        mkdir -p /home/ubuntu/.ssh
        echo '{private_key.public_key_openssh}' >> /home/ubuntu/.ssh/authorized_keys
        chmod 700 /home/ubuntu/.ssh
        chmod 600 /home/ubuntu/.ssh/authorized_keys
        chown -R ubuntu:ubuntu /home/ubuntu/.ssh
    """
)

# Create EC2 instance 4
server_4 = aws.ec2.Instance("server-4",
    ami=ami_id,
    instance_type=instance_type,
    key_name=key_pair.key_name,
    security_groups=[server_sg.name],
    tags={"Name": "server-4"},
    user_data=f"""#!/bin/bash
        mkdir -p /home/ubuntu/.ssh
        echo '{private_key.public_key_openssh}' >> /home/ubuntu/.ssh/authorized_keys
        chmod 700 /home/ubuntu/.ssh
        chmod 600 /home/ubuntu/.ssh/authorized_keys
        chown -R ubuntu:ubuntu /home/ubuntu/.ssh
    """
)

# Export Outputs
pulumi.export("server_3_public_ip", server_3.public_ip)
pulumi.export("server_4_public_ip", server_4.public_ip)
pulumi.export("security_group_id", server_sg.id)
pulumi.export("private_key_pem", pulumi.Output.secret(private_key.private_key_pem))