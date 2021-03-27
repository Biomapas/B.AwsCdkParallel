import threading

from b_continuous_subprocess.continuous_subprocess import ContinuousSubprocess

from parallel.deployment_type import DeploymentType
from parallel.error_handling_strategy import ErrorHandlingStrategy
from parallel.print_colors import PrintColors


class DeployCommand:
    def __init__(self, stack: str, deployment_type: DeploymentType):
        self.__stack = stack
        self.__deployment_type = deployment_type
        self.__ = True

    def execute(self, error_handling_strategy: ErrorHandlingStrategy, thread_event: threading.Event = None) -> None:
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
        command += ' --output=./cdk_stacks/{stack}'

        process = ContinuousSubprocess(command)
        process_generator = process.execute()

        try:
            for line in process_generator:
                if thread_event and thread_event.is_set():
                    print(
                        f'{PrintColors.WARNING}'
                        f'This thread just got an event to terminate all work!'
                        f'{PrintColors.ENDC}',
                        flush=True
                    )

                    try:
                        process.terminate()
                    except Exception as ex:
                        print(
                            f'{PrintColors.FAIL}'
                            f'Unexpected exception while terminating process: {repr(ex)}.'
                            f'{PrintColors.ENDC}',
                            flush=True
                        )
                    finally:
                        print(
                            f'{PrintColors.OKGREEN}'
                            f'This thread has finished.'
                            f'{PrintColors.ENDC}',
                            flush=True
                        )

                        return

                print(f'[{self.__stack}]   {line}')

            print(
                f'{PrintColors.OKGREEN}'
                f'Deployment of stack {self.__stack} was successful.'
                f'{PrintColors.ENDC}',
                flush=True
            )
        except Exception as ex:
            print(
                f'{PrintColors.FAIL}'
                f'Exception raised in {self.__stack} stack. Error: {repr(ex)}.'
                f'{PrintColors.ENDC}',
                flush=True
            )

            if error_handling_strategy == ErrorHandlingStrategy.RAISE:
                raise

            if error_handling_strategy == ErrorHandlingStrategy.RETRY:
                self.execute(error_handling_strategy, thread_event)
