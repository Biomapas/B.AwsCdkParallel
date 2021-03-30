from subprocess import check_call
from typing import Optional, Dict


class CdkSynth:
    @staticmethod
    def execute(
            path: Optional[str] = None,
            environment: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Synthesizes AWS CDK application and produces cdk.out directory.

        :return: No return.
        """
        check_call(['cdk', 'synth', '"*"'], cwd=path, env=environment)
