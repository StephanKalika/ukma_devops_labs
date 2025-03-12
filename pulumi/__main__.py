import pulumi
import pulumi_aws as aws

aws_region = "eu-west-1"

ec2_instance = aws.ec2.Instance(
    "example",
    ami="ami-03fd334507439f4d1",
    instance_type="t2.micro",
    tags={
        "Name": "example-instance",
    },
)

pulumi.export("public_ip", ec2_instance.public_ip)