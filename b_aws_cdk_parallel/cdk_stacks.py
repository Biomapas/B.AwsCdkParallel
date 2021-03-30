from subprocess import check_output
from typing import List, Optional, Dict


class CdkStacks:
    @staticmethod
    def list(
            cdk_application_path: Optional[str] = None,
            cdk_process_environment: Optional[Dict[str, str]] = None
    ) -> List[str]:
        """
        Lists all stacks by executing "cdk ls" command.

        :return: List of stack names for current CDK application.
        """
        output = check_output(['cdk', 'ls'], cwd=cdk_application_path, env=cdk_process_environment)
        stacks = output.decode()
        return stacks.split()
