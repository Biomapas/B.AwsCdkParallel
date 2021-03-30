import json
from typing import Optional, Dict, List

from b_aws_cdk_parallel.cdk_synth import CdkSynth


class StackDependencies:
    @staticmethod
    def generate_graph(
            path: Optional[str] = None,
            environment: Optional[Dict[str, str]] = None
    ) -> Dict[str, List[str]]:
        """
        Generates a dependency graph from a given AWS CDK application.
        It firstly synthesizes the application and then analyzes the
        manifest.json file to build a dependency tree.

        :param path: Path to AWS CDK application.
        :param environment: Process environment.

        :return: Dependency graph.
        """
        CdkSynth.execute(path, environment)

        with open(f'{path}/cdk.out/manifest.json', 'r') as file:
            data = file.read()
            data = json.loads(data)

        # Determine which are stacks and which are not.
        stacks = []
        for name, artifact in data['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                stacks.append(name)

        # Generate dependency graph.
        stack_dependency_graph = {}
        for name, artifact in data['artifacts'].items():
            if artifact['type'] == 'aws:cloudformation:stack':
                dependencies = artifact.get('dependencies', [])
                dependencies = [d for d in dependencies if d in stacks]
                stack_dependency_graph[name] = dependencies

        return stack_dependency_graph

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
