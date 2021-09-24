from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter


class MainStack(Stack):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope, id='MainStack')

        StringParameter(
            scope=self,
            id='parameter1',
            string_value='parameter1'
        )

        stack1 = Stack(
            scope=self,
            id='stack1'
       )

        StringParameter(
            scope=stack1,
            id='parameter2',
            string_value='parameter2'
        )

        stack2 = Stack(
            scope=stack1,
            id='stack2'
        )

        StringParameter(
            scope=stack2,
            id='parameter3',
            string_value='parameter3'
        )
