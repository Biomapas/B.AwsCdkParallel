from typing import List, Optional


class AwsCdkStack(object):
    def __init__(
            self,
            aws_cdk_name: str,
            pretty_name: Optional[str] = None,
            display_name: Optional[str] = None,
            dependencies: Optional[List['AwsCdkStack']] = None
    ) -> None:
        """
        Constructor.

        :param aws_cdk_name: AWS CDK generated name. Example:
            BAwsCdkParallelMainStack1BAwsCdkParallelChildStack1BAwsCdkParallelChildStack21834ED84
        :param pretty_name: Actual developer specified name. Example:
            B-Aws-Cdk-Parallel-ChildStack-2
        :param display_name: AWS CDK fully qualified name. Example:
            B-Aws-Cdk-Parallel-MainStack-1/B-Aws-Cdk-Parallel-ChildStack-1/B-Aws-Cdk-Parallel-ChildStack-2
        :param dependencies: NOT YET USED. RESERVED FOR FUTURE LINKED-LIST FEATURE.
        """
        self.aws_cdk_name = aws_cdk_name
        self.pretty_name = pretty_name
        self.display_name = display_name
        self.__dependencies = dependencies

        # Create pretty name from display name, if pretty name is not set and display name is set.
        if self.display_name:
            try:
                parts = self.display_name.split('/')
                self.pretty_name = parts[-1]
            except IndexError:
                pass

    def __str__(self):
        return self.pretty_name or self.display_name or self.aws_cdk_name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.aws_cdk_name)

    def __eq__(self, other: 'AwsCdkStack'):
        return self.aws_cdk_name == other.aws_cdk_name
