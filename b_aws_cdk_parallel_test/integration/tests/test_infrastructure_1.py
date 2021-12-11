import pytest
from b_aws_cf.exceptions.stack_does_not_exist import StackDoesNotExist
from b_aws_cf.stack import Stack
from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel_test.integration.infrastructure import path


def test_infrastructure():
    infrastructure_path = f'{path}/infrastructure1'

    executor = DeploymentExecutor(type=DeploymentType.DEPLOY, path=infrastructure_path)
    executor.run()

    # Check whether the created stacks exist.
    Stack.from_name('B-Aws-Cdk-Parallel-MainStack-1')
    Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-1')
    Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-2')

    executor = DeploymentExecutor(type=DeploymentType.DESTROY, path=infrastructure_path)
    executor.run()

    # Ensure stacks no longer exist.

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-MainStack-1')

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-1')

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-2')


def test_infrastructure_cli():
    infrastructure_path = f'{path}/infrastructure1'

    command = f'--path {infrastructure_path}'

    for line in ContinuousSubprocess(f'acdk deploy {command}').execute():
        print(line)

    # Check whether the created stacks exist.
    Stack.from_name('B-Aws-Cdk-Parallel-MainStack-1')
    Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-1')
    Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-2')

    for line in ContinuousSubprocess(f'acdk destroy {command}').execute():
        print(line)

    # Ensure stacks no longer exist.

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-MainStack-1')

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-1')

    with pytest.raises(StackDoesNotExist):
        Stack.from_name('B-Aws-Cdk-Parallel-ChildStack-2')
