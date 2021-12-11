import pytest
from b_aws_cf.exceptions.stack_does_not_exist import StackDoesNotExist
from b_aws_cf.stack import Stack
from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

from b_aws_cdk_parallel.cdk_arguments import CdkArguments
from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel_test.integration.infrastructure import path


def test_infrastructure():
    infrastructure_path = f'{path}/infrastructure4'

    cdk_arguments = CdkArguments(
        aws_cdk_app_stacks_to_deploy=['B-Aws-Cdk-Parallel-MainStack-4'],
        aws_cdk_app_parameters=[
            'TestParam1=TestValue1',
            'TestParam2=TestValue2',
            'TestParam3=TestValue3'
        ],
        aws_cdk_app_context=[
            'TestContextKey1=TestContextValue1',
            'TestContextKey2=TestContextValue2',
            'TestContextKey3=TestContextValue3'
        ]
    )

    executor = DeploymentExecutor(
        type=DeploymentType.DEPLOY,
        path=infrastructure_path,
        cdk_arguments=cdk_arguments
    )

    executor.run()

    # Check whether the created stack exists.
    Stack.from_name('B-Aws-Cdk-Parallel-MainStack-4')

    executor = DeploymentExecutor(
        type=DeploymentType.DESTROY,
        path=infrastructure_path,
        cdk_arguments=cdk_arguments
    )

    executor.run()

    # Ensure stack no longer exists.
    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-MainStack-4')


def test_infrastructure_cli():
    infrastructure_path = f'{path}/infrastructure4'

    command = (
        f'B-Aws-Cdk-Parallel-MainStack-4 '
        f'--path {infrastructure_path} '
        f'--context TestContextKey1=TestContextValue1 '
        f'--context TestContextKey2=TestContextValue2 '
        f'--context TestContextKey3=TestContextValue3 '
        f'--parameters TestParam1=TestValue1 '
        f'--parameters TestParam2=TestValue2 '
        f'--parameters TestParam3=TestValue3'
    )

    for line in ContinuousSubprocess(f'acdk deploy {command}').execute():
        print(line)

    # Check whether the created stack exists.
    Stack.from_name('B-Aws-Cdk-Parallel-MainStack-4')

    for line in ContinuousSubprocess(f'acdk destroy {command}').execute():
        print(line)

    # Ensure stack no longer exists.
    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-MainStack-4')
