import json
from typing import Optional, Dict, List, Any

from b_aws_cdk_parallel.aws_cdk_stack import AwsCdkStack
from b_aws_cdk_parallel.cdk_arguments import CdkArguments
from b_aws_cdk_parallel.cdk_synth import CdkSynth
from b_aws_cdk_parallel.color_print import multi_cprint
from b_aws_cdk_parallel.print_colors import PrintColors


class StackDependencies:
    @staticmethod
    def generate_graph(
            path: Optional[str] = None,
            environment: Optional[Dict[str, str]] = None,
            reverse_dependencies: bool = False,
            cdk_arguments: Optional[CdkArguments] = None
    ) -> Dict[AwsCdkStack, List[AwsCdkStack]]:
        """
        Generates a dependency graph from a given AWS CDK application.
        It firstly synthesizes the application and then analyzes the
        manifest.json file to build a dependency tree.

        :param path: Path to AWS CDK application.
        :param environment: Process environment.
        :param reverse_dependencies: Indicates whether a graph should contain normal dependencies
            or reversed ones. Normal dependency is represented as a word "USES". Reversed dependency
            is represented as words "IS USED BY".
        :param cdk_arguments: AWS CDK exclusive arguments.

        :return: Dependency graph.
        """
        # If path is not set, assume "current path".
        path = path or '.'

        CdkSynth.execute(path, environment, cdk_arguments)

        with open(f'{path}/cdk.out/manifest.json', 'r') as file:
            data = file.read()
            data = json.loads(data)

        graph = StackDependencies.__stack_dependency_graph(data)

        if reverse_dependencies:
            graph = StackDependencies.__reverse_dependency_graph(graph)

        return graph

    @staticmethod
    def __stack_dependency_graph(cdk_manifest_json: Dict[str, Any]) -> Dict[AwsCdkStack, List[AwsCdkStack]]:
        """
        Creates a stack dependency graph out of generated cdk manifest json file.

        :param cdk_manifest_json: CDK manifest file after running "cdk synth" command.

        :return: Stack dependency graph. Example:
            {
                "Stack1": [],    # Stack1 has no dependencies i.e Stack1 does not use other stacks.
                "Stack2": [      # Stack2 has a dependency to Stack1 i.e. Stack2 uses Stack1.
                    "Stack1"
                ],
                "Stack3": [      # Stack3 has a dependency to Stack2 i.e. Stack3 uses Stack2.
                    "Stack2"
                ],
                "Stack4": []     # Stack4 has no dependencies i.e. Stack4 does not use other stacks.
            }
        """
        # Extract all stack resources from the cdk manifest json file.
        # Create a lookup dictionary, where:
        #   Keys - are aws cdk resource (stack) names.
        #   Values - are aws cdk stack (`AwsCdkStack`) instances.
        stacks_lookup: Dict[str, AwsCdkStack] = {}
        for name, artifact in cdk_manifest_json['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                stacks_lookup[name] = AwsCdkStack(
                    aws_cdk_name=name,
                    pretty_name=artifact.get('properties', {}).get('stackName'),
                    display_name=artifact.get('displayName')
                )

        # Generate dependency graph.
        stack_dependency_graph: Dict[AwsCdkStack, List[AwsCdkStack]] = {}
        for name, artifact in cdk_manifest_json['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                # Get all of the dependencies - both stacks and other resources.
                dependencies = artifact.get('dependencies', [])
                # Filter just the stack dependencies because we don't care about other resources.
                dependencies = [stacks_lookup[d] for d in dependencies if stacks_lookup.get(d)]
                stack_dependency_graph[stacks_lookup[name]] = dependencies

        return stack_dependency_graph

    @staticmethod
    def __reverse_dependency_graph(
            stack_dependency_graph: Dict[AwsCdkStack, List[AwsCdkStack]]
    ) -> Dict[AwsCdkStack, List[AwsCdkStack]]:
        """
        Creates a reverse stack dependency graph out of created stack dependency graph.

        :param stack_dependency_graph: Created stack dependency graph.

        :return: Reverse stack dependency graph. Example (following stack dependency graph example):
        {
            "Stack1": [      # Stack1 has a reverse dependency to Stack2 i.e. Stack1 is used by Stack2.
                "Stack2"
            ],
            "Stack2": [      # Stack2 has a reverse dependency to Stack3 i.e. Stack2 is used by Stack3.
                "Stack3"
            ],
            "Stack3": [],    # Stack3 has no reverse dependencies i.e. is not used by anyone.
            "Stack4": []     # Stack4 has no reverse dependencies i.e. is not used by anyone.
        }
        """
        # Generate reverse dependency graph.
        reverse_stack_dependency_graph = {}
        for stack in stack_dependency_graph:
            reverse_stack_dependency_graph[stack] = []
            for tmp_stack, tmp_dependencies in stack_dependency_graph.items():
                if stack in tmp_dependencies:
                    reverse_stack_dependency_graph[stack].append(tmp_stack)

        return reverse_stack_dependency_graph

    @staticmethod
    def remove_dependency(
            stack: AwsCdkStack,
            stack_dependency_graph: Dict[AwsCdkStack, List[AwsCdkStack]]
    ) -> None:
        """
        Removes a given stack from the dependency graph. This function does not
        return anything. It rather has a "side effect" that modifies the
        supplied stack dependency graph.

        :param stack: Stack to be removed.
        :param stack_dependency_graph: Graph from which the stack must be removed.

        :return: No return.
        """
        if stack_dependency_graph.get(stack) is not None:
            del stack_dependency_graph[stack]

        for _, dependencies in stack_dependency_graph.items():
            if stack in dependencies:
                dependencies.remove(stack)

    @staticmethod
    def visualise_graph(stack_dependency_graph: Dict[AwsCdkStack, List[AwsCdkStack]]):
        for stack, dependencies in stack_dependency_graph.items():
            dependencies = ', '.join([str(d) for d in dependencies])
            if len(dependencies) == 0:
                multi_cprint(
                    (PrintColors.OKGREEN, '»'),
                    (PrintColors.OKBLUE, f' {stack}: [{dependencies}]')
                )
            else:
                multi_cprint(
                    (PrintColors.FAIL, '×'),
                    (PrintColors.OKBLUE, f' {stack}: [{dependencies}]')
                )
