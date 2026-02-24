# Amazon Cloud Collection for Ansible
The Amazon Cloud collection is an experimental alpha collection of auto-generated modules using the AWS Cloud Control API for interacting with AWS services.

## Contents

- [Description](#description)
- [Requirements](#requirements)
  - [Ansible version compatibility](#ansible-version-compatibility)
  - [Python version compatibility](#python-version-compatibility)
  - [AWS SDK version compatibility](#aws-sdk-version-compatibility)
- [Included content](#included-content)
- [Installation](#installation)
- [Use Cases](#use-cases)
- [Development](#development)
- [Testing](#testing)
- [Contributing to this collection](#contributing-to-this-collection)
- [Known issues](#known-issues)
- [Governance](#governance)
- [Release notes](#release-notes)
- [Support](#support)
- [Code of Conduct](#code-of-conduct)
- [More information](#more-information)
- [License Information](#license-information)

## Description

The Amazon Cloud collection's work is being made available for research purposes on the AWS Cloud Control API and community feedback on the user experience of auto-generated modules like these. Therefore, this content is not intended for production in its current state. It provides the automation capabilities needed to optimize cloud operations, ensuring efficient, reliable, and secure management of AWS resources. 

## Included content
<!--start collection content-->

See the complete list of collection content in the [Plugin Index](https://ansible-collections.github.io/amazon.cloud/branch/main/collections/amazon/cloud/index.html#plugin-index).

<!--end collection content-->

## Requirements

### Ansible version compatibility

The collection supports ansible-core versions based on `requires_ansible` in [meta/runtime.yml](meta/runtime.yml):
- This collection has been tested against Ansible Core **>=2.12.0**.

### Python version compatibility

This collection requires Python 3.9 or greater.

### AWS SDK version compatibility

Version 0.3.0 of this collection supports `boto3 >= 1.25.0` and `botocore >= 1.28.0`

## Installation

The amazon.cloud collection can be installed with the Ansible Galaxy command-line tool:

```bash
ansible-galaxy collection install amazon.cloud
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the following format:

```yaml
---
collections:
  - name: amazon.cloud
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the `ansible` package.
To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install amazon.cloud --upgrade
```

A specific version of the collection can be installed by using the `version` keyword in the `requirements.yml` file:

```yaml
---
collections:
  - name: amazon.cloud
    version: 1.0.0
```

or using the ansible-galaxy command as follows:

```bash
ansible-galaxy collection install amazon.cloud:==1.0.0
```

The python module dependencies are not installed by `ansible-galaxy`. They can be manually installed using pip:

```bash
pip install -r requirements.txt
```

Refer to the following for more details:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)


## Use Cases

You can call modules by their Fully Qualified Collection Name (FQCN), such as `amazon.cloud.logs_log_group`, or by their short name if you list the `amazon.cloud` collection in the playbook's `collections` keyword:

```yaml
---
  - name: Create log group
    amazon.cloud.logs_log_group:
      state: present
      log_group_name: "{{ log_group_name }}"
      retention_in_days: 7
      tags:
        testkey: "testvalue"
    register: log_group

  - name: Describe log group
    amazon.cloud.logs_log_group:
      state: describe
      log_group_name: "{{ log_group_name }}"
    register: output

  - name: Update log group
    amazon.cloud.logs_log_group:
      state: present
      log_group_name: "{{ log_group_name }}"
      tags:
        anotherkey: "anothervalue"
    register: output
```

Because modules may have the same name in the `amazon.cloud`, `amazon.aws`, and `community.aws` collections, we recommend using the FQCN.

For example, if you want to use the s3_bucket module without specifying the FQCN, it will use the order the collections are listed and take the first matching module it finds (in this case, s3_bucket from `amazon.aws`).

```yaml
---
  - hosts: localhost
    collections:
      - amazon.aws
      - amazon.cloud
    tasks:
      - s3_bucket:
          bucket_name: "..."
```

## Development

This collection can be generated using the [content_builder](https://github.com/ansible-community/ansible.content_builder) tool. Please refer to the [cloud_content generation section](https://github.com/ansible-community/ansible.content_builder#4-amazoncloud).

This tool can generate the api specification files and use them to generate the modules. The developer can use the [api specification](https://github.com/ansible-collections/amazon.cloud/api_specifications) files and the [modules.yaml](https://github.com/ansible-collections/amazon.cloud/modules.yaml) file hosted in this repository. The path to these files should be provided as input to the content builder tool to generate the schema and modules. To get more details on the command and input arguments please refer to the tool's [README](https://github.com/ansible-community/ansible.content_builder#resource-module-scaffolding-generated-using-openapi-based-json).

## Testing

This collection is tested using GitHub Actions. To learn more about testing, refer to [CI.md](https://github.com/ansible-collections/amazon.cloud/blob/main/CI.md).

## Contributing to this collection

We welcome community contributions to this collection. Because this collection is auto-generated using the [content_builder](https://github.com/ansible-community/ansible.content_builder) tool, if you find problems, please open an issue or create a Pull Request against the [content_builder](https://github.com/ansible-community/ansible.content_builder).

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

### More information about contributing

* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) - Details on contributing to Ansible
* [Contributing to Collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections) - How to check out collection git repositories correctly

## Known issues

* Modules are only as good as the API and its schema. Documentation may not be complete for all the modules' options and suboptions.
* Missing supportability for important AWS resources like, EC2 instance, RDS instance, EC2 volume, Elastic Load Balancer, RDS Snapshot, EC2 snapshot, etc.
* Idempotency is a function of the API and may not be fully supported.
* Missing server-side pagination. This may have severe impact on performance.
* Name-based identification filtering to support desired state (idempotency) logic is absent. This limitation has made us exclude several resources and reduce the number of modules. Client-side filtering will definitely have a large impact on performance.
* Not all the resources support the available states. In practice this means that some resources cannot be updated or listed.

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.
Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!


## Release notes

See the [rendered changelog](https://ansible-collections.github.io/amazon.cloud/branch/main/collections/amazon/cloud/docsite/CHANGELOG.html) or the [raw generated changelog](https://github.com/ansible-collections/amazon.cloud/blob/main/CHANGELOG.rst).


## Support

This is an experimental alpha collection. Community support is available through the following channels:

* Join the Ansible forum:
  * [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  * [Posts tagged with 'aws'](https://forum.ansible.com/tag/aws): subscribe to participate in collection-related conversations.
  * [AWS Working Group](https://forum.ansible.com/g/AWS): by joining the team, you will automatically be subscribed to posts tagged with [aws](https://forum.ansible.com/tags).
  * [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  * [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

* The Ansible [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.


## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## License Information

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
