# Continuous Integration (CI)

## Amazon Cloud Upstream Testing

GitHub Actions are used to run the CI for the amazon.cloud collection. The workflows used for the CI can be found in the [.github/workflows](.github/workflows) directory.

### PR Testing Workflows

The following tests run on every pull request:

| Job | Description | Python Versions | ansible-core Versions |
| --- | ----------- | --------------- | --------------------- |
| [Changelog](.github/workflows/changelog.yml) | Checks for the presence of changelog fragments | 3.9 | devel |
| [Linters](.github/workflows/linters.yml) | Runs `black` and `flake8` on plugins and tests | 3.9 | N/A |
| [Sanity](.github/workflows/sanity.yml) | Runs ansible sanity checks | See compatibility table below | devel, stable-2.17, stable-2.18, stable-2.19, stable-2.20 |
| [Unit tests](.github/workflows/units.yml) | Executes unit test cases | See compatibility table below | devel, stable-2.17, stable-2.18, stable-2.19, stable-2.20 |
| [Integration](.github/workflows/integration.yml) | Executes integration test suites | 3.11 | milestone |

**Note:** Integration tests require manual approval via the `protected` environment and AWS credentials from ansible-core-ci.

### Python Version Compatibility by ansible-core Version

These are outlined in the collection's [tox.ini](tox.ini) file (`envlist`) and GitHub Actions workflow exclusions.

| ansible-core Version | Sanity Tests | Unit Tests |
| -------------------- | ------------ | ---------- |
| devel | 3.12, 3.13, 3.14 | 3.12, 3.13 |
| stable-2.20 | 3.12, 3.13, 3.14 | 3.12, 3.13 |
| stable-2.19 | 3.11, 3.12, 3.13 | 3.11, 3.12, 3.13 |
| stable-2.18 | 3.11, 3.12, 3.13 | 3.11, 3.12, 3.13 |
| stable-2.17 | 3.10, 3.11, 3.12 | 3.10, 3.11, 3.12 |
