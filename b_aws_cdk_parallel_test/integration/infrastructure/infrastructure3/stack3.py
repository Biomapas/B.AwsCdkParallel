from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1


class Stack3(Stack):
    def __init__(self, scope: Construct, stack1: Stack1) -> None:
        super().__init__(scope=scope, id='Stack3')

        self.param = StringParameter(
            scope=self,
            id='p3',
            string_value=stack1.param.parameter_name
        )
