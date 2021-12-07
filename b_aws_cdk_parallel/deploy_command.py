import json
import subprocess
from typing import Optional, Dict

from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

from b_aws_cdk_parallel.color_print import cprint
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel.print_colors import PrintColors


class DeployCommand:
    def __init__(
            self,
            stack: str,
            type: DeploymentType,
            path: Optional[str] = None,
            env: Optional[Dict[str, str]] = None
    ):
        self.__stack = stack
        self.__deployment_type = type
        self.__path = path
        self.__env = env

    def execute(self) -> None:
        """
        Executes the CDK deployment command.

        :return: No return.
        """
        # We already know that at this stage the AWS CDK application was
        # synthesized and cdk.out directory with assets produced. Hence,
        # when deploying, we can reuse already synthesized templates with
        # assets that are in cdk.out dir. More on deployments:
        # https://taimos.de/blog/deploying-your-cdk-app-to-different-stages-and-environments
        app_stack = f'--app "cdk.out/" "{self.__stack}"'

        if self.__deployment_type == DeploymentType.DEPLOY:
            command = f'cdk deploy {app_stack}'
        elif self.__deployment_type == DeploymentType.DESTROY:
            command = f'cdk destroy {app_stack} -f'
        else:
            raise ValueError('Invalid enum value.')

        # We want to ensure that each stack deployment can have its own separate output.
        # Otherwise some clashes may start happening. Also, this approach is easier for debugging.
        command += f' --output=./cdk_stacks/{self.__stack}'
        # We want to see beautiful continuous output, hence specify progress events.
        command += ' --progress events'
        # We do not want to interact with CLI, hence add "force" flag.
        command += ' --require-approval never'
        # Don't let CDK try to deploy dependant stacks - we have that already covered by running
        # deploy command on each stack separately. This flag should massively increase deployment performance.
        command += ' --exclusively'

        cprint(PrintColors.OKBLUE, f'Executing command: {command}.')
        process = ContinuousSubprocess(command)
        process_generator = process.execute(
            path=self.__path,
            env=self.__env,
            max_error_trace_lines=50,
        )

        try:
            for line in process_generator:
                print(f'[{self.__stack}]\t{line}', end='')
            cprint(PrintColors.OKGREEN, f'Deployment of stack {self.__stack} was successful.')
        except subprocess.CalledProcessError as ex:
            cprint(PrintColors.FAIL, f'Exception raised in {self.__stack} stack. Error: {repr(ex)}.')

            error_output = json.loads(ex.output)

            # Error message.
            message = error_output['message']
            # Stack trace.
            trace = ''.join(error_output['trace'])
            # The length of a stack trace (in lines).
            trace_size = error_output['trace_size']
            # The maximum possible (allowed) length of a stack trace.
            max_trace_size = error_output['max_trace_size']

            cprint(
                PrintColors.FAIL,
                f'{trace=}\n'
                f'{message=}\n'
                f'{trace_size=}\n'
                f'{max_trace_size=}\n'
                f'{ex.returncode=}\n'
                f'{ex.cmd=}'
            )

            raise
