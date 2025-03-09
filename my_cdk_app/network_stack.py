import aws_cdk.aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "VPC",
            availability_zones=["us-east-1a", "us-east-1b"], 
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    availability_zone="us-east-1a",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet1",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    availability_zone="us-east-1a",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnet2",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    availability_zone="us-east-1b",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet2",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    availability_zone="us-east-1b",
                    cidr_mask=24
                ),
            ]
        )
