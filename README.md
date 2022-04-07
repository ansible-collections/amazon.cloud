# AWS Cloud Control Collection for Ansible
The AWS Cloud Control Collection is an experimental alpha collection of generated modules using the Cloud Control API for interacting with AWS Services. 

This content is not intended for production in its current state.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Python version compatibility

This collection requires Python 3.9 or greater.

## AWS SDK version compatibility

Version 0.1.0 of this collection supports `boto3 >= 1.20.0` and `botocore >= 1.23.0`

## Included content

<!--start collection content-->
### Modules

<!--end collection content-->

## Installing this collection

You can install the AWS Cloud Control Collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install amazon.cloud

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: amazon.cloud
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

    pip install requirements.txt

or:

    pip install boto3 botocore

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install amazon.cloud --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install amazon.cloud==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.


## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `amazon.cloud.logs_log_group`, or you can call modules by their short name if you list the `amazon.cloud` collection in the playbook's `collections` keyword:

```yaml
---
  - name: Create log group (check mode)
    amazon.cloud.logs_log_group:
      state: present
      log_group_name: "{{ log_group_name }}"
      retention_in_days: 7
      tags:
        testkey: "testvalue"
    register: log_group
```

### See Also:

* [Amazon Web Services Guide](https://docs.ansible.com/ansible/latest/scenario_guides/guide_aws.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.


## Contributing to this collection

We welcome community contributions to this collection. Because this collection is auto-generated using the [amazon_cloud_code_generator](https://github.com/ansible-collections/amazon_cloud_code_generator) tool, if you find problems, please open an issue or create a Pull Request against the [amazon_cloud_code_generator repository](https://github.com/ansible-collections/amazon_cloud_code_generator).

You can also join us on:

- IRC - the ``#ansible-aws`` [irc.libera.chat](https://libera.chat/) channel

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)


## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).


## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.
Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!


## Release notes

See the [changelog](https://github.com/ansible-collections/amazon.cloud/tree/main/CHANGELOG.rst).


## Communication

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://github.com/ansible/community/wiki/News#the-bullhorn). Be sure you are [subscribed](https://eepurl.com/gZmiEP).

Join us in the `#ansible` (general use questions and support), `#ansible-community` (community and collection development questions), and other [IRC channels](https://docs.ansible.com/ansible/devel/community/communication.html#irc-channels).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.


## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
