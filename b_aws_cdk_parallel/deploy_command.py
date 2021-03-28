import threading

from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

from b_aws_cdk_parallel.color_print import cprint
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel.error_handling_strategy import ErrorHandlingStrategy
from b_aws_cdk_parallel.print_colors import PrintColors


class DeployCommand:
    def __init__(self, stack: str, deployment_type: DeploymentType):
        self.__stack = stack
        self.__deployment_type = deployment_type

    def execute(
            self,
            error_handling_strategy: ErrorHandlingStrategy,
            thread_event: threading.Event = None,
            suppress_command_output: bool = False
    ) -> None:
        """
        Executes the CDK deployment command.

        :param error_handling_strategy: A strategy enum that tells what to do in case an error has happened.
        :param thread_event: This deployment command can be run in a separate thread and can be controlled with
            this flag. If the thread event is set - terminate the deployment.
        :return: No return.
        """
        if self.__deployment_type == DeploymentType.DEPLOY:
            command = f'cdk deploy "{self.__stack}"'
        elif self.__deployment_type == DeploymentType.DESTROY:
            command = f'cdk destroy "{self.__stack}" -f'
        else:
            raise ValueError('Invalid enum value.')

        # We want to ensure that each stack deployment can have its own output
        # because running multiple deployments in parallel usually results in
        # CDK asset errors like clashes/misses/etc.
        command += f' --output=./cdk_stacks/{self.__stack}'

        command += ' --progress events'

        cprint(PrintColors.OKBLUE, f'Executing command: {command}.')

        process = ContinuousSubprocess(command)
        process_generator = process.execute()

        try:
            for line in process_generator:
                if thread_event and thread_event.is_set():
                    cprint(PrintColors.WARNING, 'This thread just got an event to terminate all work!')
                    try:
                        process.terminate()
                    except Exception as ex:
                        cprint(PrintColors.FAIL, f'Unexpected exception while terminating process: {repr(ex)}.')
                    finally:
                        cprint(PrintColors.OKBLUE, f'This thread has finished due to a received thread event.')
                        return

                if not suppress_command_output:
                    # Print the whole output produced by an execution of the deployment command.
                    print(f'[{self.__stack}]\t{line}', end='')

            cprint(PrintColors.OKGREEN, f'Deployment of stack {self.__stack} was successful.')
        except Exception as ex:
            cprint(PrintColors.FAIL, f'Exception raised in {self.__stack} stack. Error: {repr(ex)}.')

            if error_handling_strategy == ErrorHandlingStrategy.RAISE:
                cprint(PrintColors.OKBLUE, f'Error handling is {ErrorHandlingStrategy.RAISE}, hence re-raising the exception.')
                raise

            if error_handling_strategy == ErrorHandlingStrategy.RETRY:
                cprint(PrintColors.OKBLUE, f'Error handling is {ErrorHandlingStrategy.RETRY}, hence re-running the deployment.')
                self.execute(error_handling_strategy, thread_event, suppress_command_output)
