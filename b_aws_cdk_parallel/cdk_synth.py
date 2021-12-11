from subprocess import check_call
from typing import Optional, Dict

from b_aws_cdk_parallel.cdk_arguments import CdkArguments


class CdkSynth:
    """
    Class representing an AWS CDK synth command (>>> cdk synth). Running this
    command creates cdk.out folder with synthesized CloudFormation stacks.
    """
    @staticmethod
    def execute(
            path: Optional[str] = None,
            environment: Optional[Dict[str, str]] = None,
            cdk_arguments: Optional[CdkArguments] = None
    ) -> None:
        """
        Synthesizes AWS CDK application and produces cdk.out directory.
        If the exit code was zero then return nothing, otherwise raise CalledProcessError.

        :param path: A path to an AWS CDK application.
            This path parameter is passed to the python process call.
        :param environment: OS-level environment variables, represented as dictionary,
            that are passed to the python process call.
        :param cdk_arguments: AWS CDK exclusive arguments.

        :return: No return.
        """
        cdk_arguments = cdk_arguments or CdkArguments()
        command = f'cdk synth {cdk_arguments.cli_stacks} {cdk_arguments.cli_context}'

        check_call(
            command.split(' '),
            cwd=path,
            env=environment
        )
