import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Optional, Dict

from b_aws_cdk_parallel.cdk_stacks import CdkStacks
from b_aws_cdk_parallel.color_print import cprint
from b_aws_cdk_parallel.deploy_command import DeployCommand
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel.error_handling_strategy import ErrorHandlingStrategy
from b_aws_cdk_parallel.print_colors import PrintColors
from b_aws_cdk_parallel.stack_deployment_future import StackDeploymentFuture


class DeploymentExecutor:
    def __init__(
            self,
            deployment_type: DeploymentType,
            max_thread_workers: int = 10,
            parallel_deployment_delay_seconds: int = 10,
            cdk_application_path: Optional[str] = None,
            cdk_process_environment: Optional[Dict[str, str]] = None
    ) -> None:
        self.__deployment_type = deployment_type
        self.__max_thread_workers = max_thread_workers
        self.__parallel_deployment_delay_seconds = parallel_deployment_delay_seconds
        self.__cdk_application_path = cdk_application_path
        self.__cdk_process_environment = cdk_process_environment

    def run(self) -> None:
        stacks = CdkStacks.list(self.__cdk_application_path, self.__cdk_process_environment)

        cprint(PrintColors.OKBLUE, f'Deploying stacks in parallel: {stacks}.')

        with ThreadPoolExecutor(max_workers=min(len(stacks), self.__max_thread_workers)) as executor:
            main_deployment = executor.submit(
                DeployCommand('*', self.__deployment_type, self.__cdk_application_path, self.__cdk_process_environment).execute,
                ErrorHandlingStrategy.RETRY_IF_POSSIBLE
            )

            cprint(PrintColors.OKGREEN, 'Successfully created main deployment future.')

            stack_futures: List[StackDeploymentFuture] = []
            for stack in stacks:
                # If the main deployment is not running (it means it has finished),
                # there is no reason to run side deployments. Skip side deployments
                # and immediately check what was the status of a finished main deployment.
                if not main_deployment.running():
                    cprint(PrintColors.WARNING, 'The main deployment is not running. Skipping side deployments.')
                    break

                future = StackDeploymentFuture()
                future.stack_name = stack
                future.thread_event = threading.Event()
                future.future_object = executor.submit(
                    DeployCommand(stack, self.__deployment_type, self.__cdk_application_path, self.__cdk_process_environment).execute,
                    ErrorHandlingStrategy.RETRY,
                    future.thread_event,
                    True,
                    True
                )

                cprint(PrintColors.OKGREEN, f'Successfully created {stack} stack deployment future.')

                stack_futures.append(future)
                time.sleep(self.__parallel_deployment_delay_seconds)

            try:
                main_deployment.result()
                exception = main_deployment.exception()

                if exception:
                    cprint(PrintColors.FAIL, f'The main deployment has failed! Reason: {repr(exception)}.')
                else:
                    cprint(PrintColors.OKGREEN, 'The main deployment successfully finished.')
            except Exception as ex:
                exception = ex
                cprint(PrintColors.FAIL, f'The main deployment has failed due unknown error! Reason: {repr(ex)}.')
            finally:
                for future in stack_futures:
                    cprint(PrintColors.WARNING, f'Cancelling future: {future.stack_name}.')
                    # Cancel the future that is not yet running or is completed.
                    future.future_object.cancel()
                    # Instruct the future to terminate all work and exist asap.
                    future.thread_event.set()

            cprint(PrintColors.OKBLUE, 'Exiting deployment workflow in 5 seconds...')
            time.sleep(5)

            if exception:
                raise exception
