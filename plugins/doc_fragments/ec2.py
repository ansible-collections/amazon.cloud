# Copyright: (c) 2022, Ansible, Inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    # EC2 only documentation fragment
    DOCUMENTATION = r"""
options:
    region:
        description:
          - The AWS region to use. If not specified then the value of the AWS_REGION or EC2_REGION environment variable, if any, is used.
            See U(http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region)
        type: str
        aliases: [ aws_region, ec2_region ]
"""
