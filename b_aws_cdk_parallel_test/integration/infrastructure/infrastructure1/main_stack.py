from aws_cdk.aws_ssm import StringParameter
from aws_cdk.core import Stack, Construct


class MainStack(Stack):
    """
    Stack to test basic functionality.
    """

    def __init__(self, scope: Construct) -> None:
        stack_name = 'B-Aws-Cdk-Parallel-MainStack-1'
        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        StringParameter(
            scope=self,
            id='parameter1',
            string_value='parameter1'
        )

        stack_name = 'B-Aws-Cdk-Parallel-ChildStack-1'
        stack1 = Stack(
            scope=self,
            id=stack_name,
            stack_name=stack_name
        )

        StringParameter(
            scope=stack1,
            id='parameter2',
            string_value='parameter2'
        )

        stack_name = 'B-Aws-Cdk-Parallel-ChildStack-2'
        stack2 = Stack(
            scope=stack1,
            id=stack_name,
            stack_name=stack_name
        )

        StringParameter(
            scope=stack2,
            id='parameter3',
            string_value='parameter3'
        )
