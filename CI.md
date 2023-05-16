# CI

## Code validation workflows

GitHub Actions are used to run the Continuous Integration for amazon.cloud collection. The workflows used for the CI can be found [here](https://github.com/ansible-collections/amazon.cloud/tree/main/.github/workflows). These workflows include jobs to run the unit tests, integration tests, sanity tests, linters, changelog check and doc related checks. The following table lists the python and ansible versions against which these jobs are run.

| Jobs              | Description                                    | Python Versions      | Ansible Versions                                                    |
| ----------------- | ---------------------------------------------- | -------------------- | ------------------------------------------------------------------- |
| changelog         | Checks for the presence of Changelog fragments | 3.9                  | devel                                                               |
| Linters           | Runs `black` and `flake8` on plugins and tests | 3.9                  | devel                                                               |
| Sanity            | Runs ansible sanity checks                     | 3.8, 3.9, 3.10, 3.11 | Stable-2.12, 2.13, 2.14 (not on py 3.11), Stable-2.15+ (not on 3.8) |
| Unit tests        | Executes the unit test cases                   | 3.9, 3.10            | Stable-2.12+                                                        |
| Integration tests | Executes the integration test suites           | 3.9                  | devel                                                               |

## Release worflows

These workflows include jobs to validate galaxy importer, manually create release, push release tag and publish collection to ansible galaxy. The following table lists the workflows and how they are triggered.

| Jobs            | Description                                          | trigger                                         |
| --------------- | ---------------------------------------------------- | ----------------------------------------------- |
| galaxy/importer | validate that collection can be imported into galaxy | pull request/push/schedule                      |
| Release/prepare | Create a new release pull request                    | manual trigger by repository admin              |
| Release/tag     | Publish repository tag                               | pull request [closed] with label 'ok-to-tag'    |
| Release/publish | Publish release to galaxy                            | release [published] (when a new tag is created) |
