import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Optional, Dict

from b_aws_cdk_parallel.aws_cdk_stack import AwsCdkStack
from b_aws_cdk_parallel.cdk_arguments import CdkArguments
from b_aws_cdk_parallel.color_print import cprint
from b_aws_cdk_parallel.deploy_command import DeployCommand
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_cdk_parallel.print_colors import PrintColors
from b_aws_cdk_parallel.stack_dependencies import StackDependencies


class DeploymentExecutor:
    def __init__(
            self,
            type: DeploymentType,
            path: Optional[str] = None,
            env: Optional[Dict[str, str]] = None,
            max_parallel_deployments: Optional[int] = None,
            cdk_arguments: Optional[CdkArguments] = None
    ) -> None:
        """
        Constructor.

        :param type: Deployment type. Usually it is either DEPLOY or DESTROY.
        :param path: Path to the AWS CDK application.
        :param env: OS-level environment variables.
        :param max_parallel_deployments: Maximum amount of parallel deployments at the same time.
        :param cdk_arguments: AWS CDK exclusive arguments.
        """
        self.__type = type
        self.__path = path
        self.__env = env
        self.__max_parallel_deployments = max_parallel_deployments or 100
        self.__cdk_arguments = cdk_arguments or CdkArguments()

    def run(self):
        cprint(PrintColors.OKBLUE, 'Starting to deploy stacks...\n')
        time_seconds_start = time.time()
        self.__run()
        time_seconds_end = time.time()
        time_delta = int(time_seconds_end - time_seconds_start)
        cprint(PrintColors.OKBLUE, f'\nTotal deployment time: {time_delta} seconds.\n')

    def __run(self, stack_dependency_graph: Optional[Dict[AwsCdkStack, List[AwsCdkStack]]] = None) -> None:
        if stack_dependency_graph is not None and len(stack_dependency_graph) == 0:
            cprint(PrintColors.OKBLUE, 'No more stacks to deploy. Exiting...')
            return

        # DESTROY - REVERSE GRAPH. If we are destroying stacks, we want to generate a reverse dependency graph.
        # It is because we firstly want to destroy all stacks that are not used by other stacks.
        # DEPLOY - NORMAL GRAPH. If we are deploying stacks, we want to generate a normal dependency graph.
        # It is because we firstly want to deploy all stacks that don't use other stacks.
        is_reverse_graph = True if self.__type == DeploymentType.DESTROY else False

        # Reuse dependency graph or create a new one.
        stack_dependency_graph = stack_dependency_graph or StackDependencies.generate_graph(
            path=self.__path,
            environment=self.__env,
            reverse_dependencies=is_reverse_graph,
            cdk_arguments=self.__cdk_arguments
        )

        print('\n')
        cprint(PrintColors.OKBLUE, '----- Stack dependency graph: -----')
        StackDependencies.visualise_graph(stack_dependency_graph)
        print('\n')

        futures_pool = []
        deployable_stacks = []
        max_workers = min(self.__max_parallel_deployments, len(stack_dependency_graph))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for stack, dependencies in stack_dependency_graph.items():
                if len(dependencies) == 0:
                    cprint(PrintColors.OKBLUE, f'Stack {str(stack)} has no dependencies, deploying...')
                    deployable_stacks.append(stack)
                    futures_pool.append(executor.submit(
                        DeployCommand(
                            stack=stack,
                            type=self.__type,
                            path=self.__path,
                            env=self.__env,
                            cdk_arguments=self.__cdk_arguments
                        ).execute,
                    ))

            for future in futures_pool:
                future.result()

        for stack in deployable_stacks:
            cprint(PrintColors.OKBLUE, f'Removing stack {str(stack)} from the graph as it was successfully deployed...')
            StackDependencies.remove_dependency(stack, stack_dependency_graph)

        self.__run(stack_dependency_graph)
