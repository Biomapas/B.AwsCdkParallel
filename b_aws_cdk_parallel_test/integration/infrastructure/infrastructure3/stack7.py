from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack2 import Stack2
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack3 import Stack3
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack4 import Stack4
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack5 import Stack5


class Stack7(Stack):
    def __init__(
            self,
            scope: Construct,
            stack1: Stack1,
            stack2: Stack2,
            stack3: Stack3,
            stack4: Stack4,
            stack5: Stack5
    ) -> None:
        super().__init__(scope=scope, id='Stack7')

        self.p1 = StringParameter(
            scope=self,
            id='p1',
            string_value=stack1.param.parameter_name
        )

        self.p2 = StringParameter(
            scope=self,
            id='p2',
            string_value=stack2.param.parameter_name
        )

        self.p3 = StringParameter(
            scope=self,
            id='p3',
            string_value=stack3.param.parameter_name
        )

        self.p4 = StringParameter(
            scope=self,
            id='p4',
            string_value=stack4.param2.parameter_name
        )

        self.p5 = StringParameter(
            scope=self,
            id='p5',
            string_value=stack5.param1.parameter_name
        )
