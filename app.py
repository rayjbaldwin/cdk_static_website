#!/usr/bin/env python3
import os
import aws_cdk as cdk
from my_cdk_app.network_stack import NetworkStack
from my_cdk_app.server_stack import ServerStack


app = cdk.App()
network_stack = NetworkStack(app, "NetworkStack")
server_stack = ServerStack(app, "ServerStack", vpc=network_stack.vpc)
app.synth()

