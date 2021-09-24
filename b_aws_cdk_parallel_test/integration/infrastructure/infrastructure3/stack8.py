from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter


class Stack8(Stack):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope, id='Stack8')

        self.param = StringParameter(
            scope=self,
            id='p1',
            string_value='p1'
        )
