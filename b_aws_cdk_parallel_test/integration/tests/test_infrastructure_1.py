# from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
# from b_aws_cdk_parallel.deployment_type import DeploymentType
# from b_aws_cdk_parallel_test.integration.infrastructure import path
#
#
# def test_infrastructure():
#     infrastructure_path = f'{path}/infrastructure1'
#
#     executor = DeploymentExecutor(type=DeploymentType.DEPLOY, path=infrastructure_path)
#     executor.run()
#
#     executor = DeploymentExecutor(type=DeploymentType.DESTROY, path=infrastructure_path)
#     executor.run()
