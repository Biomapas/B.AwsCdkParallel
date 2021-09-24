from aws_cdk.core import App

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure2.main_stack import MainStack

app = App()
MainStack(app)
app.synth()
