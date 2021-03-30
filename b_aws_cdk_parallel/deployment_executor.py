import json
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Optional, Dict

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
            env: Optional[Dict[str, str]] = None
    ) -> None:
        self.__type = type
        self.__path = path
        self.__env = env

    def run(self, stack_dependency_graph: Optional[Dict[str, List[str]]] = None) -> None:
        if stack_dependency_graph is not None and len(stack_dependency_graph) == 0:
            cprint(PrintColors.OKBLUE, 'No more stacks to deploy. Exiting...')
            return

        stack_dependency_graph = stack_dependency_graph or StackDependencies.generate_graph(self.__path, self.__env)
        cprint(PrintColors.OKBLUE, f'Stack dependency graph:\n{json.dumps(stack_dependency_graph, indent=4)}.')

        futures_pool = []
        deployable_stacks = []
        with ThreadPoolExecutor(max_workers=len(stack_dependency_graph.keys())) as executor:
            for stack, dependencies in stack_dependency_graph.items():
                if len(dependencies) == 0:
                    cprint(PrintColors.OKBLUE, f'Stack {stack} has no dependencies, deploying...')
                    deployable_stacks.append(stack)
                    futures_pool.append(executor.submit(
                        DeployCommand(
                            stack=stack,
                            type=self.__type,
                            path=self.__path,
                            env=self.__env
                        ).execute,
                    ))

            for future in futures_pool:
                future.result()

        for stack in deployable_stacks:
            cprint(PrintColors.OKBLUE, f'Removing stack {stack} from the graph as it was successflu deployed...')
            StackDependencies.remove_dependency(stack, stack_dependency_graph)

        self.run(stack_dependency_graph)
