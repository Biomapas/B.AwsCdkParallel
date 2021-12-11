from typing import Optional, List


class CdkArguments:
    """
    Container class that wraps arguments that are exclusive for AWS CDK.
    """
    def __init__(
            self,
            aws_cdk_app_stacks_to_deploy: Optional[List[str]] = None,
            aws_cdk_app_parameters: Optional[List[str]] = None,
            aws_cdk_app_context: Optional[List[str]] = None
    ) -> None:
        self.aws_cdk_app_stacks_to_deploy = aws_cdk_app_stacks_to_deploy

        self.__assert_key_value_pairs(aws_cdk_app_parameters)
        self.aws_cdk_app_parameters = aws_cdk_app_parameters

        self.__assert_key_value_pairs(aws_cdk_app_context)
        self.aws_cdk_app_context = aws_cdk_app_context

    @staticmethod
    def __assert_key_value_pairs(list_of_pairs: Optional[List[str]] = None) -> None:
        if list_of_pairs is None:
            return

        for pair in list_of_pairs:
            try:
                key, value = pair.split('=')
                assert key is not None
                assert value is not None
            except (AssertionError, ValueError):
                raise ValueError(f'Bad key/value pair supplied: {pair}. Must be in format: key=value.')

    @property
    def cli_stacks(self) -> str:
        return ' '.join(self.aws_cdk_app_stacks_to_deploy or ['--all'])

    @property
    def cli_parameters(self) -> str:
        params = [f'--parameters {p}' for p in self.aws_cdk_app_parameters or []]
        return ' '.join(params)

    @property
    def cli_context(self) -> str:
        context = [f'--context {c}' for c in self.aws_cdk_app_context or []]
        return ' '.join(context)

    @property
    def cli(self) -> str:
        args = [self.cli_stacks]
        if self.cli_parameters: args.append(self.cli_parameters)
        if self.cli_context: args.append(self.cli_context)

        return ' '.join(args)
