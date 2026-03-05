# Continuous Integration (CI)

## AWS Upstream Testing

GitHub Actions are used to run the CI for the amazon.cloud collection. The workflows used for the CI can be found [here](https://github.com/ansible-collections/amazon.cloud/tree/main/.github/workflows). These workflows include jobs to run the unit tests, sanity tests, linters, and changelog checks.

The collection uses reusable workflows from [ansible-network/github_actions](https://github.com/ansible-network/github_actions) for standardized testing.

To learn more about the testing strategy, see [this proposal](https://github.com/ansible-collections/cloud-content-handbook/blob/main/Proposals/core_collection_dependency.md).

### PR Testing Workflows

The following tests run on every pull request:

| Job | Description | Python Versions | ansible-core Versions |
| --- | ----------- | --------------- | --------------------- |
| Changelog | Checks for the presence of changelog fragments | Standard | devel |
| Linters | Runs `black` and `flake8` on plugins and tests via tox | Standard | devel |
| Sanity | Runs ansible sanity checks | See compatibility table below | devel, stable-2.17, stable-2.18, stable-2.19, stable-2.20 |
| Unit tests | Executes unit test cases | See compatibility table below | devel, stable-2.17, stable-2.18, stable-2.19, stable-2.20 |
| Integration tests | Executes integration test suites (requires manual approval) | 3.11 | milestone |

### Python Version Compatibility by ansible-core Version

These are determined by the reusable workflows from [ansible-network/github_actions](https://github.com/ansible-network/github_actions) and the collection's [tox.ini](/tox.ini) file.

| ansible-core Version | Sanity Tests | Unit Tests |
| -------------------- | ------------ | ---------- |
| devel | 3.12, 3.13, 3.14 | 3.12, 3.13 |
| stable-2.20 | 3.12, 3.13, 3.14 | 3.12, 3.13 |
| stable-2.19 | 3.11, 3.12, 3.13 | 3.11, 3.12, 3.13 |
| stable-2.18 | 3.11, 3.12, 3.13 | 3.11, 3.12, 3.13 |
| stable-2.17 | 3.10, 3.11, 3.12 | 3.10, 3.11, 3.12 |

### Integration Test Requirements

Integration tests for amazon.cloud require:
- Manual approval via the `protected` environment in GitHub Actions
- AWS credentials provisioned via ansible-core-ci
- Python 3.11 with milestone ansible-core version

The integration workflow uses `pull_request_target` for secure credential handling and runs after approval.

### Minimum Requirements

- **ansible-core**: >=2.12.0 (per [meta/runtime.yml](meta/runtime.yml))
- **Python**: >=3.9
- **boto3**: >=1.25.0
- **botocore**: >=1.28.0
- **Dependencies**: amazon.aws >=6.0.0, community.aws >=5.3.0

## Release Workflows

These workflows include jobs to validate galaxy importer, manually create release, push release tag and publish collection to ansible galaxy.

| Job | Description | Trigger |
| --- | ----------- | ------- |
| galaxy_importer | Validate that collection can be imported into galaxy | pull request/push/schedule |
| Release/prepare | Create a new release pull request | Manual trigger by repository admin |
| Release/tag | Publish repository tag | Pull request [closed] with label 'ok-to-tag' |
| Release/publish | Publish release to galaxy | Release [published] (when a new tag is created) |
