# Amazon Cloud Collection for Ansible
The AWS Cloud Control Collection is an experimental alpha collection of generated modules using the Cloud Control API for interacting with AWS Services.

## Description

AWS Cloud Control Collection's work is being made available for research purposes on the Cloud Control API and community feedback on the user experience of API generated module like these. Therefore, this content is not intended for production in its current state.
It provides the automation capabilities needed to optimize cloud operations, ensuring efficient, reliable, and secure management of AWS resources. 

## Included content
<!--start collection content-->

See the complete list of collection content in the [Plugin Index](https://ansible-collections.github.io/amazon.cloud/branch/main/collections/amazon/cloud/index.html#plugin-index).

<!--end collection content-->

## Requirements

<!--start requires_ansible-->
### Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.12.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Python version compatibility

This collection requires Python 3.9 or greater.

### AWS SDK version compatibility

Version 0.3.0 of this collection supports `boto3 >= 1.25.0` and `botocore >= 1.28.0`

## Installation

A specific version of the AWS Cloud Control Collection can be installed with Ansible Galaxy command-line tool:
```bash
    ansible-galaxy collection install amazon.cloud==1.0.0
```

It can also included in a `requirements.yml` file and installed with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: amazon.cloud
    version: 1.0.0
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install requirements.txt

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install amazon.cloud --upgrade
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.


## Use Cases

You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `amazon.cloud.logs_log_group`, or you can call modules by their short name if you list the `amazon.cloud` collection in the playbook's `collections` keyword:

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

Because modules may keep the same name in the `amazon.cloud`, `amazon.aws` and `community.aws` collections, we recommend using the FQCN.

For example, if you want to use the s3_bucket module without specyfing the FQDN, it will use the order the collections are listed and take the first matching module it finds (in this case, s3_bucket from `amazon.aws`).

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

## Developement

This collection can be generated using the [content_builder](https://github.com/ansible-community/ansible.content_builder) tool. Please refer to the [cloud_content generation section](https://github.com/ansible-community/ansible.content_builder#4-amazoncloud).

This tool can generate the api specification files and use them to generate the modules. The developer can use the [api specification](https://github.com/ansible-collections/amazon.cloud/api_specifications) files and the [modules.yaml](https://github.com/ansible-collections/amazon.cloud/modules.yaml) file hosted in this repository. The path to these files should be provided as input to the content builder tool to generate the schema and modules. To get more details on the command and input arguments please refer to the tool's [README](https://github.com/ansible-community/ansible.content_builder#resource-module-scaffolding-generated-using-openapi-based-json).

## Testing

This collection is tested using GitHub Actions. To know more on testing, refer to [CI.md](https://github.com/ansible-collections/amazon.cloud/blob/main/CI,md).

## Contributing to this collection

We welcome community contributions to this collection. Because this collection is auto-generated using the [content_builder](https://github.com/ansible-community/ansible.content_builder) tool, if you find problems, please open an issue or create a Pull Request against the [content_builder](https://github.com/ansible-community/ansible.content_builder).

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Known issues

* Modules are only as good as the API and its schema. Documentation may not be complete for all the modules' options and suboptions.
* Missing supportability for important AWS resources like, EC2 instance, RDS instance, EC2 volume, Elastic Load Balancer, RDS Snapshot, EC2 snapshot, etc.
* Idempotency is a function of the API and may not be fully supported.
* Missing server-side pagination. This may have severe impact on performance.
* Name-based identification filtering to support desired state (idempotency) logic is absent. This limitation has made us to exclude several resources and reduce the numebr of modules. A client-side filtering will definitely have a large impact on performance.
* Not all the resources support the available states. In practice this means that some resources cannot be updated or listed.

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.
Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!


## Release notes

See the [rendered changelog](https://ansible-collections.github.io/amazon.cloud/branch/main/collections/amazon/cloud/docsite/CHANGELOG.html) or the [raw generated changelog](https://github.com/ansible-collections/amazon.cloud/tree/main/CHANGELOG.rst).


## Support

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

For the latest supported versions, refer to the release notes below.

If you encounter issues or have questions, you can submit a support request through the following channels:
 - GitHub Issues: Report bugs, request features, or ask questions by opening an issue in the [GitHub repository]((https://github.com/ansible-collections/amazon.cloud/).
 - Ansible Community: Engage with the Ansible community on the Ansible Project Mailing List or [Ansible Forum](https://forum.ansible.com/g/AWS).

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.


## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Amazon.Cloud Collection Guide](https://docs.ansible.com/ansible/latest/scenario_guides/guide_amazon_cloud.html)
- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## License Information

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
