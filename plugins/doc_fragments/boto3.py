# -*- coding: utf-8 -*-

# Copyright: (c) 2022,  Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):

    # Minimum requirements for the collection
    DOCUMENTATION = r'''
options: {}
requirements:
  - python >= 3.9
  - boto3 >= 1.20.0
  - botocore >= 1.23.0
  - jsonpatch
'''
