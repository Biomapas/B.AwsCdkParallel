import json
from typing import Optional, Dict, List, Any

from b_aws_cdk_parallel.cdk_synth import CdkSynth


class StackDependencies:
    @staticmethod
    def generate_graph(
            path: Optional[str] = None,
            environment: Optional[Dict[str, str]] = None,
            reverse_dependencies: bool = False
    ) -> Dict[str, List[str]]:
        """
        Generates a dependency graph from a given AWS CDK application.
        It firstly synthesizes the application and then analyzes the
        manifest.json file to build a dependency tree.

        :param path: Path to AWS CDK application.
        :param environment: Process environment.
        :param reverse_dependencies: Indicates whether a graph should contain normal dependencies
            or reversed ones. Normal dependency is represented as a word "USES". Reversed dependency
            is represented as words "IS USED BY".

        :return: Dependency graph.
        """
        CdkSynth.execute(path, environment)

        with open(f'{path}/cdk.out/manifest.json', 'r') as file:
            data = file.read()
            data = json.loads(data)

        graph = StackDependencies.__stack_dependency_graph(data)

        if reverse_dependencies:
            graph = StackDependencies.__reverse_dependency_graph(graph)

        return graph

    @staticmethod
    def __stack_dependency_graph(cdk_manifest_json: Dict[str, Any]) -> Dict[str, List[str]]:
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
        # Determine which are stacks and which are not.
        stacks = []
        for name, artifact in cdk_manifest_json['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                stacks.append(name)

        # Generate dependency graph.
        stack_dependency_graph = {}
        for name, artifact in cdk_manifest_json['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                # Get all of the dependencies - both stacks and other resources.
                dependencies = artifact.get('dependencies', [])
                # Filter just the stack dependencies because we don't care about other resources.
                dependencies = [d for d in dependencies if d in stacks]
                stack_dependency_graph[name] = dependencies

        return stack_dependency_graph

    @staticmethod
    def __reverse_dependency_graph(stack_dependency_graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
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
    def remove_dependency(stack: str, stack_dependency_graph: Dict[str, List[str]]) -> None:
        """
        Removes a given stack from the dependency graph. This function does not
        return anything. It rather has a "side effect" that modifies the
        supplied stack dependency graph.

        :param stack: Stack name to be removed.
        :param stack_dependency_graph: Graph from which the stack must be removed.

        :return: No return.
        """
        if stack_dependency_graph.get(stack) is not None:
            del stack_dependency_graph[stack]

        for _, dependencies in stack_dependency_graph.items():
            if stack in dependencies:
                dependencies.remove(stack)
