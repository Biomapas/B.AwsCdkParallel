# B.AwsCdkParallel

A python based package that enables AWS CDK parallel stack deployments.

### Description

One of the biggest downsides of AWS CDK IaC tool is the sequential deployments.
If you have many stacks within your project - it can take hours and hours till
everything gets deployed. Wouldn't it be cool to parallelize them? According to 
AWS CDK tool maintainers - they are not even thinking right now to include such 
functionality. Hence, this project was built. This project allows you to run 
traditional `cdk deploy *` and `cdk destroy * -f`. But the main trick is that it 
can do it in parallel - massively increasing the speed of your deployments.

### Remarks

[Biomapas](https://biomapas.com) aims to modernise life-science 
industry by sharing its IT knowledge with other companies and 
the community. This is an open source library intended to be used 
by anyone. Improvements and pull requests are welcome.

Some techniques and inspirations were taken from this blog post:<br>
https://taimos.de/blog/deploying-your-cdk-app-to-different-stages-and-environments

General issue is being discussed on github:<br>
https://github.com/aws/aws-cdk/issues/1973

### Related technology

- Python 3
- AWS CDK
- AWS CloudFormation

### Assumptions

The project assumes the following:

- You have basic-good knowledge in python programming.
- You have basic-good knowledge in AWS.
- You have very good knowledge in AWS CDK.

### Useful sources

- Read more AWS CDK:<br>
https://github.com/aws/aws-cdk
  
- Read more about parallel AWS CDK deployments:<br>
https://taimos.de/blog/deploying-your-cdk-app-to-different-stages-and-environments

### Install

The project is built and uploaded to PyPi. Install it by using pip.

```
pip install b_aws_cdk_parallel
```

Or directly install it through source.

```
pip install .
```

### Usage & Examples

#### Programmatic usage

To start deployment programmatically:

```python
from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType

executor = DeploymentExecutor(
    type=DeploymentType.DEPLOY,
    path='/optional/path/to/cdk/app',
    env={
        'optional': 'os-level environment variables'
    }
)

executor.run()
```

To start stacks destruction programmatically:

```python
from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType

executor = DeploymentExecutor(
    type=DeploymentType.DESTROY,
    path='/optional/path/to/cdk/app',
    env={
        'optional': 'os-level environment variables'
    }
)

executor.run()
```

#### CLI usage

The library also exposes CLI access. 

To get usage help, simply run:

```
acdk -h
```

To deploy infrastructure, run:

```
acdk deploy --path /project/app/
```

To destroy infrastructure, run:

```
acdk destroy --path /project/app/
```

### Testing

This project has integration tests based on pytest. To run tests, simply run:

```
pytest b_aws_cdk_parallel_test/integration/tests
```

### Contribution

Found a bug? Want to add or suggest a new feature?<br>
Contributions of any kind are gladly welcome. You may contact us 
directly, create a pull-request or an issue in github platform.
Lets modernize the world together.
