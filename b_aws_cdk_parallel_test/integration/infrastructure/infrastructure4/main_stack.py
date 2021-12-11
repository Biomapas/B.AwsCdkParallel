from aws_cdk.aws_ssm import StringParameter
from aws_cdk.core import Stack, Construct, CfnParameter


class MainStack(Stack):
    """
    Stack to test context and parameters functionalities.
    """
    def __init__(self, scope: Construct) -> None:
        stack_name = 'B-Aws-Cdk-Parallel-MainStack-4'
        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        StringParameter(
            scope=self,
            id='p1',
            string_value=scope.node.try_get_context('TestContextKey1')
        )

        StringParameter(
            scope=self,
            id='p2',
            string_value=self.node.try_get_context('TestContextKey2')
        )

        StringParameter(
            scope=self,
            id='p3',
            string_value=self.node.try_get_context('TestContextKey3')
        )

        test_parameter1 = CfnParameter(
            scope=self,
            id="TestParam1",
            type="String",
            description="Test parameter."
        )

        test_parameter2 = CfnParameter(
            scope=self,
            id="TestParam2",
            type="String",
            description="Test parameter."
        )

        test_parameter3 = CfnParameter(
            scope=self,
            id="TestParam3",
            type="String",
            description="Test parameter."
        )

        StringParameter(
            scope=self,
            id='parameter2',
            string_value=(
                test_parameter1.value_as_string +
                test_parameter2.value_as_string +
                test_parameter3.value_as_string
            )
        )
