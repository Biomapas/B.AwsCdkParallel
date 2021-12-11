import argparse

from b_aws_cdk_parallel.cdk_arguments import CdkArguments
from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType


def main():
    arg_parser = argparse.ArgumentParser(description='Asynchronous AWS CDK deployment executor.')

    choices = [c.lower() for c in DeploymentType.to_string_list()]

    arg_parser.add_argument(
        'action',
        choices=choices,
        help=f'AWS CDK action. Choices: {choices}.'
    )

    # Adding support for specifying stacks as per
    # https://github.com/Biomapas/B.AwsCdkParallel/issues/4 issue.
    arg_parser.add_argument(
        'stacks',
        nargs='*',
        action='extend',
        help=(
            'CDK stacks to deploy. '
            'Example: PipelineStack LambdaStack or more advanced like "*Stack". '
            'If nothing is specified - "all stacks" is assumed.'
        )
    )

    arg_parser.add_argument(
        '--path',
        nargs='?',
        help='CDK app path. Example: --path /project/app/.',
        default=None
    )

    # Adding support for parameters arguments as per
    # https://github.com/Biomapas/B.AwsCdkParallel/issues/1 issue.
    arg_parser.add_argument(
        '--parameters',
        nargs='*',
        action='extend',
        help='Parameters for CDK app. Example: --parameters uploadBucketName=UpBucket.',
    )

    # Adding support for context arguments as per
    # https://github.com/Biomapas/B.AwsCdkParallel/issues/1 issue.
    arg_parser.add_argument(
        '--context',
        nargs='*',
        action='extend',
        help='Context for CDK app. Example: --context key1=value1.',
    )

    params = arg_parser.parse_args()

    cdk_arguments = CdkArguments(
        aws_cdk_app_stacks_to_deploy=params.stacks,
        aws_cdk_app_parameters=params.parameters,
        aws_cdk_app_context=params.context
    )

    DeploymentExecutor(
        type=DeploymentType[params.action.upper()],
        path=params.path,
        cdk_arguments=cdk_arguments
    ).run()
