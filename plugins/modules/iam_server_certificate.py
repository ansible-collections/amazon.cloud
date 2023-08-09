#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated using the ansible.content_builder.
# See: https://github.com/ansible-community/ansible.content_builder


DOCUMENTATION = r"""
module: iam_server_certificate
short_description: Uploads and manages a server certificate entity for the AWS account
description:
- Uploads and manages a server certificate entity for the AWS account.
options:
    certificate_body:
        aliases:
        - CertificateBody
        description:
        - Not Provived.
        type: str
    certificate_chain:
        aliases:
        - CertificateChain
        description:
        - Not Provived.
        type: str
    force:
        default: false
        description:
        - Cancel IN_PROGRESS and PENDING resource requestes.
        - Because you can only perform a single operation on a given resource at a
            time, there might be cases where you need to cancel the current resource
            operation to make the resource available so that another operation may
            be performed on it.
        type: bool
    path:
        aliases:
        - Path
        description:
        - Not Provived.
        type: str
    private_key:
        aliases:
        - PrivateKey
        description:
        - Not Provived.
        type: str
    purge_tags:
        default: true
        description:
        - Remove tags not listed in I(tags).
        type: bool
    server_certificate_name:
        aliases:
        - ServerCertificateName
        description:
        - Not Provived.
        type: str
    state:
        choices:
        - present
        - absent
        - list
        - describe
        - get
        default: present
        description:
        - Goal state for resource.
        - I(state=present) creates the resource if it doesn't exist, or updates to
            the provided state if the resource already exists.
        - I(state=absent) ensures an existing instance is deleted.
        - I(state=list) get all the existing resources.
        - I(state=describe) or I(state=get) retrieves information on an existing resource.
        type: str
    tags:
        aliases:
        - Tags
        - resource_tags
        description:
        - A dict of tags to apply to the resource.
        - To remove all tags set I(tags={}) and I(purge_tags=true).
        type: dict
    wait:
        default: false
        description:
        - Wait for operation to complete before returning.
        type: bool
    wait_timeout:
        default: 320
        description:
        - How many seconds to wait for an operation to complete before timing out.
        type: int
author: Ansible Cloud Team (@ansible-collections)
version_added: 0.2.0
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2
- amazon.cloud.boto3
"""

EXAMPLES = r"""
- name: Load the certificate data
  set_fact:
    cert_a_data: '{{ lookup("file", path_cert_a) }}'
    cert_b_data: '{{ lookup("file", path_cert_b) }}'
    chain_cert_data: '{{ lookup("file", path_intermediate_cert) }}'

- name: Create Certificate
  amazon.cloud.iam_server_certificate:
    server_certificate_name: '{{ cert_name }}'
    state: present
    certificate_body: '{{ cert_a_data }}'
    private_key: '{{ lookup("file", path_cert_key) }}'
    wait: true
  register: create_cert

- name: Delete certificate
  amazon.cloud.iam_server_certificate:
    server_certificate_name: '{{ cert_name }}'
    state: absent
  register: delete_cert

- name: Create Certificate with Chain and path
  amazon.cloud.iam_server_certificate:
    server_certificate_name: '{{ cert_name }}'
    state: present
    certificate_body: '{{ cert_a_data }}'
    private_key: '{{ lookup("file", path_cert_key) }}'
    certificate_chain: '{{ chain_cert_data }}'
    path: /example/
  register: create_cert

- name: Gather information about a certificate
  amazon.cloud.iam_server_certificate:
    server_certificate_name: '{{ cert_name }}'
    state: get
  register: create_info
"""

RETURN = r"""
result:
    description:
        - When I(state=list), it is a list containing dictionaries of resource information.
        - Otherwise, it is a dictionary of resource information.
        - When I(state=absent), it is an empty dictionary.
    returned: always
    type: complex
    contains:
        identifier:
            description: The unique identifier of the resource.
            type: str
        properties:
            description: The resource properties.
            type: dict
"""


from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    AnsibleAmazonCloudModule,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    CloudControlResource,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    ansible_dict_to_boto3_tag_list,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import (
    scrub_none_parameters,
)
from ansible_collections.amazon.cloud.plugins.module_utils.core import map_key_to_alias
from ansible_collections.amazon.cloud.plugins.module_utils.core import camel_to_snake


def main():
    argument_spec = dict(
        state=dict(
            type="str",
            choices=["present", "absent", "list", "describe", "get"],
            default="present",
        ),
    )

    argument_spec["certificate_body"] = {"type": "str", "aliases": ["CertificateBody"]}
    argument_spec["certificate_chain"] = {
        "type": "str",
        "aliases": ["CertificateChain"],
    }
    argument_spec["server_certificate_name"] = {
        "type": "str",
        "aliases": ["ServerCertificateName"],
    }
    argument_spec["path"] = {"type": "str", "aliases": ["Path"]}
    argument_spec["private_key"] = {"type": "str", "aliases": ["PrivateKey"]}
    argument_spec["tags"] = {"type": "dict", "aliases": ["Tags", "resource_tags"]}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["present", "absent", "list", "describe", "get"],
        "default": "present",
    }
    argument_spec["wait"] = {"type": "bool", "default": False}
    argument_spec["wait_timeout"] = {"type": "int", "default": 320}
    argument_spec["force"] = {"type": "bool", "default": False}
    argument_spec["purge_tags"] = {"type": "bool", "default": True}

    required_if = [
        ["state", "present", ["server_certificate_name"], True],
        ["state", "absent", ["server_certificate_name"], True],
        ["state", "get", ["server_certificate_name"], True],
    ]
    mutually_exclusive = []

    module = AnsibleAmazonCloudModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    cloud = CloudControlResource(module)

    type_name = "AWS::IAM::ServerCertificate"

    params = {}

    params["certificate_body"] = module.params.get("certificate_body")
    params["certificate_chain"] = module.params.get("certificate_chain")
    params["path"] = module.params.get("path")
    params["private_key"] = module.params.get("private_key")
    params["server_certificate_name"] = module.params.get("server_certificate_name")
    params["tags"] = module.params.get("tags")

    # The DesiredState we pass to AWS must be a JSONArray of non-null values
    _params_to_set = scrub_none_parameters(params)

    # Only if resource is taggable
    if module.params.get("tags") is not None:
        _params_to_set["tags"] = ansible_dict_to_boto3_tag_list(module.params["tags"])

    # Use the alias from argument_spec as key and avoid snake_to_camel conversions
    params_to_set = map_key_to_alias(_params_to_set, argument_spec)

    # Ignore createOnlyProperties that can be set only during resource creation
    create_only_params = [
        "/properties/ServerCertificateName",
        "/properties/PrivateKey",
        "/properties/CertificateBody",
        "/properties/CertificateChain",
    ]

    # Necessary to handle when module does not support all the states
    handlers = ["create", "read", "update", "delete", "list"]

    state = module.params.get("state")
    identifier = ["/properties/ServerCertificateName"]

    results = {"changed": False, "result": {}}

    if state == "list":
        if "list" not in handlers:
            module.exit_json(
                **results, msg=f"Resource type {type_name} cannot be listed."
            )
        results["result"] = cloud.list_resources(type_name, identifier)

    if state in ("describe", "get"):
        if "read" not in handlers:
            module.exit_json(
                **results, msg=f"Resource type {type_name} cannot be read."
            )
        results["result"] = cloud.get_resource(type_name, identifier)

    if state == "present":
        results = cloud.present(
            type_name, identifier, params_to_set, create_only_params
        )

    if state == "absent":
        results["changed"] |= cloud.absent(type_name, identifier)

    module.exit_json(**results)


if __name__ == "__main__":
    main()
