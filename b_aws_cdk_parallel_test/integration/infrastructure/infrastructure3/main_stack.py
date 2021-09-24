from aws_cdk.core import Stack, Construct

from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack1 import Stack1
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack10 import Stack10
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack2 import Stack2
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack3 import Stack3
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack4 import Stack4
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack5 import Stack5
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack6 import Stack6
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack7 import Stack7
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack8 import Stack8
from b_aws_cdk_parallel_test.integration.infrastructure.infrastructure3.stack9 import Stack9


class MainStack(Stack):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope, id='MainStack')

        s1 = Stack1(self)
        s2 = Stack2(self, s1)
        s3 = Stack3(self, s1)
        s4 = Stack4(self, s1, s2, s3)
        s5 = Stack5(self, s1, s4)
        s7 = Stack7(self, s1, s2, s3, s4, s5)
        s6 = Stack6(self, s1, s7)
        s8 = Stack8(s7)
        s9 = Stack9(self, s1, s8)
        Stack10(s9, s1, s6, s7)
