from subprocess import check_output
from typing import List


class CdkStacks:
    @staticmethod
    def list() -> List[str]:
        """
        Lists all stacks by executing "cdk ls" command.

        :return: List of stack names for current CDK application.
        """
        output = check_output(['cdk', 'ls'])
        stacks = output.decode()
        return stacks.split()
