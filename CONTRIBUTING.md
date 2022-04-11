# Contributing

## Getting Started

General information about setting up your Python environment, testing modules,
Ansible coding styles, and more can be found in the [Ansible Community Guide](
https://docs.ansible.com/ansible/latest/community/index.html).

Information about AWS SDK library usage, module utils, testing, and more can be
found in the [AWS Guidelines](https://docs.ansible.com/ansible/devel/dev_guide/platforms/aws_guidelines.html)
documentation.

## AWS Collections

There are three related collections containing AWS content (modules and plugins).

### amazon.cloud
The AWS Cloud Control Collection is an experimental alpha collection of generated modules using the Cloud Control API for interacting with AWS Services. 

The `amazon.cloud` collection is an [Ansible-maintained collection](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html).

### amazon.aws
This collection contains the `module_utils` (shared libraries) used by all the AWS collections.
Content in this collection is included downstream in Red Hat Ansible Automation Platform.

Code standards, test coverage, and other supportability criteria may be higher in this collection. 

The `amazon.aws` collection is an [Ansible-maintained collection](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html).

### community.aws
This collection contains modules and plugins contributed and maintained by the Ansible AWS
community.  The `community.aws` collection is tested and generally assured to work in
conjunction with `amazon.aws`.

New modules and plugins developed by the community should be proposed to `community.aws`.
Content in this collection that is stable and meets other acceptance criteria has the potential
to be promoted and migrated into `amazon.aws`.

## Submitting Issues 

All software has bugs, and the `amazon.cloud` collection is no exception.  When you find a bug, 
you can help tremendously by [telling us about it](https://github.com/ansible-collections/amazon.cloud/issues/new/choose).

If you should discover that the bug you're trying to file already exists in an issue, 
you can help by verifying the behavior of the reported bug with a comment in that 
issue, or by reporting any additional information

## Pull Requests

Because this collection is auto-generated using the [amazon_cloud_code_generator](https://github.com/ansible-collections/amazon_cloud_code_generator) tool, if you find problems, please, don't open Pull Requests against this repository. Pull Requests needs to be created gainst the [amazon_cloud_code_generator repository](https://github.com/ansible-collections/amazon_cloud_code_generator).

You don't know how to start? Refer to our [amazon_cloud_code_generator contribution guidelines](https://github.com/ansible-collections/amazon_cloud_code_generator/blob/main/CONTRIBUTING.md)!

## Code of Conduct
The `amazon.cloud` collection follows the Ansible project's 
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html). 
Please read and familiarize yourself with this document.

## IRC
Our IRC channels may require you to register your nickname. If you receive an error when you connect, see 
[Libera.Chat's Nickname Registration guide](https://libera.chat/guides/registration) for instructions.

The `#ansible-aws` channel on [irc.libera.chat](https://libera.chat/) is the main and official place to discuss use and development
of the `amazon.cloud` collection.
