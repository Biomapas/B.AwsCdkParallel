import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from parallel.cdk_stacks import CdkStacks
from parallel.deploy_command import DeployCommand
from parallel.deployment_type import DeploymentType
from parallel.error_handling_strategy import ErrorHandlingStrategy
from parallel.stack_deployment_future import StackDeploymentFuture


class DeploymentExecutor:
    def __init__(
            self,
            deployment_type: DeploymentType,
            max_thread_workers: int = 10,
            parallel_deployment_delay_seconds: int = 10
    ):
        self.__deployment_type = deployment_type
        self.__max_thread_workers = max_thread_workers
        self.__parallel_deployment_delay_seconds = parallel_deployment_delay_seconds

    def run(self) -> None:
        stacks = CdkStacks.list()

        with ThreadPoolExecutor(max_workers=min(len(stacks), self.__max_thread_workers)) as executor:
            main_deployment = executor.submit(
                DeployCommand('*', self.__deployment_type).execute,
                ErrorHandlingStrategy.RAISE
            )

            stack_futures: List[StackDeploymentFuture] = []
            for stack in stacks:
                # If the main deployment is not running (it means it has finished),
                # there is no reason to run side deployments. Skip side deployments
                # and immediately check what was the status of a finished main deployment.
                if not main_deployment.running():
                    print(f'The main deployment is not running. Skipping side deployments.', flush=True)
                    break

                future = StackDeploymentFuture()
                future.stack_name = stack
                future.thread_event = threading.Event()
                future.future_object = executor.submit(
                    DeployCommand(stack, self.__deployment_type).execute,
                    ErrorHandlingStrategy.RETRY
                )

                stack_futures.append(future)
                time.sleep(self.__parallel_deployment_delay_seconds)

            try:
                main_deployment.result()
                print(f'The main deployment successfully finished.', flush=True)
            except Exception as ex:
                print(f'The main deployment has failed! Reason: {repr(ex)}.', flush=True)
            finally:
                for future in stack_futures:
                    # Cancel the future that is not yet running or is completed.
                    future.future_object.cancel()
                    # Instruct the future to terminate all work and exist asap.
                    future.thread_event.set()
