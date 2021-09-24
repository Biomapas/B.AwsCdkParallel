from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack2 import Stack2
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack3 import Stack3


class Stack4(Stack):
    def __init__(self, scope: Construct, stack1: Stack1, stack2: Stack2, stack3: Stack3) -> None:
        super().__init__(scope=scope, id='Stack4')

        self.param1 = StringParameter(
            scope=self,
            id='p1',
            string_value=stack1.param.parameter_name
        )

        self.param2 = StringParameter(
            scope=self,
            id='p2',
            string_value=stack2.param.parameter_name
        )

        self.param3 = StringParameter(
            scope=self,
            id='p3',
            string_value=stack3.param.parameter_name
        )
