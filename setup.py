from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_aws_cdk_parallel',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_aws_cdk_parallel_test'
    ]),
    description=(
        'Package that enables deployment of AWS CDK stacks in parallel.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'acdk=b_aws_cdk_parallel.cli.acdk:main',
        ],
    },
    install_requires=[
        'pytest',
        'attrs>=21.0.0',
        'aws-cdk.core>=1.90.0',
        'aws-cdk.aws-ssm>=1.90.0',
        'b-continuous-subprocess>=0.3.2,<1.0.0',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='AWS IAC CDK Parallel',
    url='https://github.com/biomapas/B.AwsCdkParallel.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
