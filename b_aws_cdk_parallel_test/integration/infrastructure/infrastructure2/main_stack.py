from aws_cdk.core import Stack, Construct
from aws_cdk.aws_ssm import StringParameter


class MainStack(Stack):
    """
    Stack to test basic functionality.
    """
    def __init__(self, scope: Construct) -> None:
        stack_name = 'B-Aws-Cdk-Parallel-MainStack-2'
        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        stack1 = Stack(
            scope=self,
            id='stack1'
        )

        parameter1 = StringParameter(
            scope=stack1,
            id='parameter1',
            string_value='parameter1'
        )

        stack2 = Stack(
            scope=self,
            id='stack2'
        )

        parameter2 = StringParameter(
            scope=stack2,
            id='parameter2',
            string_value=parameter1.parameter_name
        )

        stack3 = Stack(
            scope=self,
            id='stack3'
        )

        StringParameter(
            scope=stack3,
            id='parameter3',
            string_value=parameter2.parameter_name
        )
