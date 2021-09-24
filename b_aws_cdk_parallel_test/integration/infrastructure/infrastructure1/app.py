from aws_cdk.core import App

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure1.main_stack import MainStack

app = App()
MainStack(app)
app.synth()
