from aws_cdk import  Stack, RemovalPolicy
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
from aws_cdk.aws_ec2 import InstanceType
import aws_cdk.aws_rds as rds

class ServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
# Web servers' security group opens port 80 from anywhere

        web_sg = ec2.SecurityGroup(self, "WebSG",
            vpc=vpc,
            allow_all_outbound=True,
        )
        web_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
        )   
        
# RDS instance's security group opens port 3306 to only web servers' security group
        
        rds_sg = ec2.SecurityGroup(self, "RDS_SG",
            vpc=vpc,
            allow_all_outbound=True,
        )
        rds_sg.add_ingress_rule(
            web_sg,
            ec2.Port.tcp(3306),
        )
        
# Launch one web server in each public subnets

        public_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        key_pair = ec2.KeyPair.from_key_pair_name(self, "KeyPair", "baldwinr-ec2-seis615")

        ec2.Instance(self, "Web Server 1",
            vpc=vpc,
            instance_type=InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=web_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[public_subnets.subnets[0]]
            ),
            key_pair=key_pair

        )
        
        ec2.Instance(self, "Web Server 2",
            vpc=vpc,
            instance_type=InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            security_group=web_sg,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[public_subnets.subnets[1]]
            ),
            key_pair=key_pair
        )          

# A RDS instance with MySQL engine with all private subnets as its subnet group.
        
        rds_subnet_group = rds.SubnetGroup(self, "RDSSubnet",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            description="Subnet for RDS"
        )

        rds_instance = rds.DatabaseInstance(self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_39),
            vpc=vpc,
            storage_type=rds.StorageType.GP2,
            security_groups=[rds_sg],
            subnet_group=rds_subnet_group,
            removal_policy=RemovalPolicy.DESTROY,
            allocated_storage=20
        )
