from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack7 import Stack7


class Stack6(Stack):
    def __init__(self, scope: Construct, stack1: Stack1, stack7: Stack7) -> None:
        super().__init__(scope=scope, id='Stack6')

        self.param1 = StringParameter(
            scope=self,
            id='p1',
            string_value=stack1.param.parameter_name
        )

        self.param2 = StringParameter(
            scope=self,
            id='p2',
            string_value=stack7.p1.parameter_name
        )
