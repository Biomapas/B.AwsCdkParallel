import argparse

from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType


def main():
    arg_parser = argparse.ArgumentParser(description='Asynchronous AWS CDK deployment executor.')

    choices = [DeploymentType.DEPLOY.name, DeploymentType.DESTROY.name]
    choices = [c.lower() for c in choices]

    arg_parser.add_argument(
        'action',
        choices=choices,
        help=f'AWS CDK action. Choices: {choices}.'
    )

    arg_parser.add_argument(
        '--path',
        nargs='?',
        help='CDK app path. Example: --path /project/app/.',
        default=None
    )

    params = arg_parser.parse_args()

    DeploymentExecutor(
        type=DeploymentType[params.action.upper()],
        path=params.path,
    ).run()
