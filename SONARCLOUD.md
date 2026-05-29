# SonarQube Cloud in amazon.cloud

SonarQube Cloud (SonarCloud) is a Software-as-a-Service (SaaS) code analysis tool that helps maintain code quality by identifying issues related to maintainability, reliability, and security.

The amazon.cloud collection uses SonarQube Cloud to analyze the main branch and pull requests, and to track unit test coverage and quality gate compliance.

## Core concepts

1. **Clean as You Code**: Development practice where new code must meet quality standards.

2. **Clean Code Attributes**: Consistency, Intentionality, Adaptability, and Responsibility. See [Code analysis metrics](https://docs.sonarsource.com/sonarqube-cloud/digging-deeper/metric-definitions/).

3. **Software Quality**: SonarQube Cloud evaluates quality by flagging issues that violate clean code principles.

4. **Quality Standards**: Defined by a quality profile (rules) and a quality gate (conditions that must pass). The gate shows pass or fail based on whether all conditions are met.

## Analysis method: CI-based analysis

The collection uses **CI-based analysis** with GitHub Actions:

- The SonarScanner runs inside the CI build.
- Configuration is controlled in the repository (`sonar-project.properties` and `.github/workflows/sonarcloud.yml`).
- **Code coverage** is produced by a dedicated coverage job in `all_green` and passed to the scanner via a `coverage` artifact (see [Coverage integration](#coverage-integration) below).

Automatic analysis is not used because it does not support code coverage and has limited branch support.

References:

- [CI-Based Analysis overview](https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/overview-of-integrated-cis/)
- [Test coverage in SonarCloud](https://docs.sonarsource.com/sonarqube-cloud/enriching/test-coverage/overview/)

## Configuration files

### `sonar-project.properties`

Project-level analysis settings live in `sonar-project.properties` at the repository root:

| Parameter | Value | Purpose |
|-----------|--------|---------|
| `sonar.projectKey` | `ansible-collections_amazon.cloud` | SonarCloud project identifier |
| `sonar.organization` | `ansible-collections` | SonarCloud organization |
| `sonar.projectName` | `amazon.cloud` | Display name |
| `sonar.sources` | `.` | Root of analyzed source tree |
| `sonar.tests` | `tests/unit,tests/integration` | Test directories (for test-aware analysis) |
| `sonar.exclusions` | `tests/**,.tox/**` | Paths excluded from analysis |
| `sonar.python.coverage.reportPaths` | `coverage.xml` | Default coverage report path (overridden by CI when present) |
| `sonar.python.version` | `3.9` | Python version for analysis (matches collection minimum) |
| `sonar.newCode.referenceBranch` | `main` | Branch used as baseline for "new code" |

The project key **must match** the SonarCloud UI exactly when the project is created (**Analyze new project** → select this repository).

Full reference: [Analysis parameters](https://docs.sonarqube.org/latest/analysis/analysis-parameters/).

## GitHub Actions integration

### Reusable SonarCloud workflow (`workflow_call`)

`.github/workflows/sonarcloud.yml` defines a **reusable** workflow (`on: workflow_call`) aligned with [kubernetes.core](https://github.com/ansible-collections/kubernetes.core) ([PR #1124](https://github.com/ansible-collections/kubernetes.core/pull/1124)). It is **not** self-triggering: the **`all_green`** aggregator will invoke it after linters, sanity, units, and a **coverage** job succeed.

The scan job:

1. Checks out the repository at the PR head commit (on pull requests) or `github.sha` (on push).
2. Downloads the **`coverage`** artifact from the same workflow run (when present).
3. Discovers `coverage*.xml` files and sets `sonar.python.coverage.reportPaths` when any are found.
4. Prepares SonarScanner arguments (`sonar.scm.revision`, PR metadata on pull requests).
5. Runs [SonarSource/sonarqube-scan-action](https://github.com/SonarSource/sonarqube-scan-action) with `SONAR_TOKEN` from the org secret `ANSIBLE_COLLECTIONS_ORG_SONAR_TOKEN_CICD_BOT`.

### Why `workflow_call` (not `workflow_run`)

- **Checkout**: The caller's `pull_request` / `push` event allows `actions/checkout` to use `github.event.pull_request.head.sha` on PRs, which SonarCloud expects for pull request analysis.
- **Artifacts**: Coverage is uploaded in the same workflow run as the gate; the reusable job uses `actions/download-artifact@v4` with `name: coverage`.
- **Secrets**: The caller passes only the required org secret explicitly (do not use `secrets: inherit` when GitHub reports that only required secrets may be passed).

### Fork pull requests and secrets

GitHub **does not** expose org/repository secrets to workflows triggered by pull requests **from forks** the same way as for branches on the same repository. Sonar jobs that need `SONAR_TOKEN` therefore run for:

- Pushes to `main` and `stable-*` on this repository, and
- Pull requests whose head branch is on **ansible-collections/amazon.cloud** (not from a fork).

Fork PRs may skip Sonar until changes are merged or a maintainer runs analysis from a trusted branch. See [Using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) and [Approving workflow runs from forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/approving-workflow-runs-from-public-forks).

## Coverage integration

Coverage integration is now complete:

1. A **coverage** job in `.github/workflows/all_green_check.yml` produces Cobertura XML and uploads it as artifact **`coverage`**.
2. The **`all_green`** gate depends on **coverage** completion.
3. A **`sonarcloud`** job calls `./.github/workflows/sonarcloud.yml` with explicit `secrets:` for `ANSIBLE_COLLECTIONS_ORG_SONAR_TOKEN_CICD_BOT`.

CI now runs SonarCloud scans automatically on pull requests and pushes to `main` and `stable-*` branches. You can also validate configuration with the SonarScanner CLI locally (see [Debugging SonarCloud issues](#debugging-sonarcloud-issues) below).

## Summary

| Component | File | Status |
|-----------|------|--------|
| Sonar project settings | `sonar-project.properties` | Present |
| Reusable scanner workflow | `.github/workflows/sonarcloud.yml` | Present (`workflow_call` only) |
| `all_green` coverage + Sonar caller | `.github/workflows/all_green_check.yml` | Complete |

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| `all_green` | `.github/workflows/all_green_check.yml` | `pull_request`, push to `main` / `stable-*` | Linters, sanity, units, coverage; gate on success |
| SonarCloud | `.github/workflows/sonarcloud.yml` | `workflow_call` from `all_green` | Download coverage artifact and run SonarScanner |

## Debugging SonarCloud issues

If analysis fails or coverage is missing:

1. **Check `all_green`**: Ensure the workflow (including the **coverage** job) succeeded for the same commit.
2. **Check artifact**: In the SonarCloud run, confirm the download and "Set coverage report paths" steps found at least one `coverage*.xml` and set `COVERAGE_PATHS`.
3. **Run SonarScanner locally**: Install [SonarScanner CLI](https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-cli/), set `SONAR_TOKEN` from [SonarCloud Security](https://sonarcloud.io/account/security), and run from the repo root:

   ```sh
   sonar-scanner -Dsonar.projectBaseDir=. -Dsonar.host.url=https://sonarcloud.io
   ```

   Fix any errors reported at the end of the output.

*Note:* Use the SonarCloud project page and local `sonar-scanner` runs to verify settings if analysis results are unexpected.

## Prerequisites (org admins)

Before CI can upload analysis:

1. Create the SonarCloud project and link it to **ansible-collections/amazon.cloud**; set the project key to **`ansible-collections_amazon.cloud`**.
2. Ensure the org secret **`ANSIBLE_COLLECTIONS_ORG_SONAR_TOKEN_CICD_BOT`** is available to repository workflows.

## References

- [SonarCloud Documentation](https://docs.sonarsource.com/sonarqube-cloud/)
- [GitHub Actions for SonarCloud](https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud/)
- [Storing and sharing workflow data (artifacts)](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow)
- [Reusing workflows (`workflow_call`)](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- Related community doc: [SonarQube Cloud in amazon.aws](https://github.com/ansible-collections/amazon.aws/blob/main/sonarcloud.md)
