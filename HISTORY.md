# Release history

### 3.2.0
* Remove `aws-cdk.core` dependency as it is probably not needed (if the project is developed
  with AWS CDK anyways it will have `core` module installed). By removing this dependency both
  `V1` and `V2` versions of AWS CDK should work.

### 3.1.0
* Fix dependencies.
* Remove unnecessary dependencies.

### 3.0.0
* cdk v2 compatibility.
* Use the stack displayName when calling the cdk deploy command.

### 2.3.0
* Improve parallel stack deployments by introducing `--exclusively` flag.
* Make dependencies graph beautiful.
* Output beautiful stack names (not aws cdk generated names).
* Fix --path CLI bug.

### 2.2.0
* Support "--parameters".
* Support "--context".
* Support specifying stacks.
* Add a lot more tests.

### 2.1.0
* Expose CLI command `acdk` to enable deployment/destruction through CLI.

### 2.0.0
* Major bug fixes for resolving stack dependencies. The algorithm for parallel stack destruction has fundamentally changed.
* Added integration tests to test against an actual AWS environment.
* More improvements will come for 2.1.0.

### 1.3.0
* Do not rebuild assets on destroy.

### 1.2.0
* Do not rebuild assets on deployment.

### 1.1.0
* Add ability to control maximum parallel deployments.

### 1.0.0
* Complete rework of the project. Build a dependency tree to determine what to deploy.

### 0.4.1
* Raise exception in case of a failed deployment.

### 0.4.0
* Cdk list command should also receive path and environment.

### 0.3.0
* Add ability to specify CDK path and environment variables for processes.

### 0.2.0
* Add ability to retry main deployment too.

### 0.1.0
* Refactor project to make it more debug-friendly.

### 0.0.2
* Upgrade dependencies.

### 0.0.1
* Initial build.
