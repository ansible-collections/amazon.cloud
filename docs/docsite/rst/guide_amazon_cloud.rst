.. _ansible_collections.amazon.cloud.docsite.aws_intro:

*************************
Amazon Web Services Guide
*************************

The AWS Cloud Control Collection ``amazon.cloud`` is an experimental alpha collection that contains a number of generated modules using the Cloud Control API for controlling Amazon Web Services (AWS). This guide explains how to use the modules to automate your AWS resources with Ansible.

.. contents::
   :local:

Requirements for the AWS modules are minimal.

All of the modules require and are tested against recent versions of botocore and boto3.

Python 3.9 or greater will be required.

Whereas classically Ansible will execute tasks in its host loop against multiple remote machines, most cloud-control steps occur on your local machine with reference to the regions to control.

In your playbook steps we'll typically be using the following pattern for provisioning steps::

    - hosts: localhost
      gather_facts: False
      tasks:
        - ...

.. _ansible_collections.amazon.cloud.docsite.aws_authentication:

Authentication
``````````````

Authentication with the AWS-related modules is handled by either
specifying your access and secret key as ENV variables or module arguments.

For environment variables::

    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

For storing these in a vars_file, ideally encrypted with ansible-vault::

    ---
    aws_access_key: "--REMOVED--"
    aws_secret_key: "--REMOVED--"

Note that if you store your credentials in vars_file, you need to refer to them in each AWS-module. For example::

    - amazon.cloud.logs_log_group:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        log_group_name: "..."

Or they can be specified using "module_defaults" at the top of a playbook.::

    # demo_setup.yml

    - hosts: localhost
      module_defaults:
        group/aws:
          aws_access_key: '{{ aws_access_key }}'
          aws_secret_key: '{{ aws_secret_key }}'
          region: '{{ region }}'
      tasks:
        - amazon.cloud.logs_log_group:
            log_group_name: "..."

Credentials can also be accessed from a `Credentials Profile <https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_profiles.html>`_.::

    - amazon.cloud.logs_log_group:
        aws_profile: default
        log_group_name: "..."

.. _ansible_collections.amazon.cloud.docsite.aws_provisioning:

Provisioning
````````````

The s3_bucket module provisions and de-provisions S3 buckets.

An example of creating an S3 bucket with public access block configuration follows.

Additional tags can be specified with the "tags" parameter.::

    # demo_setup.yml

    - hosts: localhost
      gather_facts: False

      tasks:

        - name: Provision an S3 bucket with a with public added block configuration
          amazon.aws.s3_bucket:
            bucket_name: Demo
            public_access_block_configuration:
                block_public_acls: true
                block_public_policy: true
                ignore_public_acls: true
                restrict_public_buckets: true
            tags:
              Environment: Testing
          register: result

The data about the S3 bucket that has been created is being saved by the "register" keyword in the variable named "result".

.. _ansible_collections.amazon.cloud.docsite.aws_next_steps:

Next Steps: Explore Modules
```````````````````````````

Ansible ships with lots of modules for configuring a wide array of AWS services.  Browse the "Cloud" category of the module
documentation for a full list with examples.

.. seealso::

   :ref:`list_of_collections`
       Browse existing collections, modules, and plugins
   :ref:`working_with_playbooks`
       An introduction to playbooks
   :ref:`playbooks_delegation`
       Delegation, useful for working with loud balancers, clouds, and locally executed steps.
   `User Mailing List <https://groups.google.com/group/ansible-devel>`_
       Have a question?  Stop by the google group!
   `irc.libera.chat <https://libera.chat/>`_
       #ansible IRC chat channel
