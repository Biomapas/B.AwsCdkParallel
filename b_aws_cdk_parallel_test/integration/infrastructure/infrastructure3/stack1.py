from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter


class Stack1(Stack):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope, id='Stack1')

        self.param = StringParameter(
            scope=self,
            id='p1',
            string_value='p1'
        )
