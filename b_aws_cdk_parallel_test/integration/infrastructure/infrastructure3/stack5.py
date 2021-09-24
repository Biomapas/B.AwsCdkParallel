from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack4 import Stack4


class Stack5(Stack):
    def __init__(self, scope: Construct, stack1: Stack1, stack4: Stack4) -> None:
        super().__init__(scope=scope, id='Stack5')

        self.param1 = StringParameter(
            scope=self,
            id='p1',
            string_value=stack1.param.parameter_name
        )

        self.param2 = StringParameter(
            scope=self,
            id='p2',
            string_value=stack4.param1.parameter_name
        )

        self.param3 = StringParameter(
            scope=self,
            id='p3',
            string_value=stack4.param2.parameter_name
        )
