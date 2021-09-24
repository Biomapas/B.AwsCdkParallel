from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack8 import Stack8


class Stack9(Stack):
    def __init__(self, scope: Construct, stack1: Stack1, stack8: Stack8) -> None:
        super().__init__(scope=scope, id='Stack9')

        self.param1 = StringParameter(
            scope=self,
            id='p1',
            string_value='p1'
        )

        self.param2 = StringParameter(
            scope=self,
            id='p2',
            string_value=stack1.param.parameter_name
        )

        self.param3 = StringParameter(
            scope=self,
            id='p3',
            string_value=stack8.param.parameter_name
        )
