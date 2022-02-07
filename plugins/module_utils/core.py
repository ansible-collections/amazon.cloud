#
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2021 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
This module_utility adds shared support for AWS Cloud Control API modules.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import logging

logging.basicConfig(filename='/Users/alinabuzachis/dev/example.log', level=logging.DEBUG)

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - " "%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


import botocore
import json

from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code
from ansible_collections.amazon.cloud.plugins.module_utils.utils import diff_dict


class CloudControlResource(object):

    def __init__(self, module):
        """
        Until we can use a connection plugin for auth and client setup, reuse AnsibleAWSModule
        """
        self.module = module
        self.client = module.client('cloudcontrol', retry_decorator=AWSRetry.jittered_backoff())

    def list_resources(self, type_name):
        """
        An exception occurred during task execution. To see the full traceback, use -vvv.
        The error was: botocore.exceptions.OperationNotPageableError: Operation cannot be paginated: list_resources
        """
        try:
            response = self.client.list_resources(TypeName=type_name)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg="")
        return response
    
    def list_resource_requests(self, params):
        """
        Returns existing resource operation requests using specific filters.
        Resource operation requests expire after seven days.
        """
        try:
            response = self.client.list_resource_requests(**params)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg="")
        return response

    def get_resource(self, type_name, primary_identifier):
        # This is the "describe" equivalent for CCAPI
        try:
            response = self.client.get_resource(TypeName=type_name, Identifier=primary_identifier)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg="")
        return response

    def create_resource(self, type_name, identifier, params):
        result = {"changed": False, "result": {}}
        try:
            response = self.client.get_resource(TypeName=type_name, Identifier=identifier)
            result["result"] = response
        except self.client.exceptions.ResourceNotFoundException:
            try:
                response = self.client.create_resource(TypeName=type_name, DesiredState=params)
                self.client.get_waiter('resource_request_success').wait(RequestToken=response['ProgressEvent']['RequestToken'])
            except botocore.exceptions.WaiterError as e:
                self.module.fail_json_aws(e, msg='An error occurred waiting for the resource request to become successful')
            result["changed"] = True
            result["result"] = response
            self.module.exit_json(**result)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg="")
        return result
    

    def check_in_progress_requesst(self, type_name, identifier):
        in_progress_requests= []
        params = {
            'ResourceRequestStatusFilter' : {
                'Operations': ['CREATE', 'DELETE', 'UPDATE'],
                'OperationStatuses': ['IN_PROGRESS', ]
            }
        }

        try:
            response = self.client.list_resource_requests(**params)
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg='')

        if response.get('ResourceRequestStatusSummaries'):
            in_progress_requests = list(filter(lambda d: d['TypeName'] == type_name and  d['Identifier'] == identifier, response['ResourceRequestStatusSummaries']))

            if in_progress_requests:
                self.module.warn(f"There is one or more IN PROGRESS operations on {identifier}. Wait until there are no more IN PROGRESS operations before proceding.")
                for e in in_progress_requests: self.client.get_waiter('resource_request_success').wait(RequestToken=e['RequestToken'])
        
        return


    def delete_resource(self, type_name, identifier):
        result = {"changed": False, "result": {}}
        response = {}

        self.check_in_progress_requesst(type_name, identifier)

        try:
            response = self.client.get_resource(TypeName=type_name, Identifier=identifier)
        except self.client.exceptions.ResourceNotFoundException:
            return result

        try:
            response = self.client.delete_resource(TypeName=type_name, Identifier=identifier)
            if self.module.params.get('wait'):
                try:
                    self.client.get_waiter('resource_request_success').wait(RequestToken=response['ProgressEvent']['RequestToken'])
                except botocore.exceptions.WaiterError as e:
                    self.module.fail_json_aws(e, msg='An error occurred waiting for the resource request to become successful.')
            result["changed"] = True
            result["result"] = response
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg='')
        
        return result

    def update_resource(self, type_name, identifier, params):
        result = {"changed": False, "result": {}}

        self.check_in_progress_requesst(type_name, identifier)
    
        try:
            response = self.client.get_resource(TypeName=type_name, Identifier=identifier)
        except self.client.exceptions.ResourceNotFoundException:
            return result
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            self.module.fail_json_aws(e, msg="")
        
        properties = response.get('ResourceDescription', {}).get('Properties', {})
        properties = json.loads(properties)
        
        to_be_updated = diff_dict(properties, params)
        
        def _format_patch(data):
            params = []
            for key in data.keys():
                result = {"op": "replace", "path": key, "value": data[key]}
                params.append(result)
            return json.dumps(params)

        if to_be_updated:
            try:
                response = self.client.update_resource(TypeName=type_name, Identifier=identifier, PatchDocument=_format_patch(to_be_updated))
                if self.module.params.get('wait'):
                    try:
                        self.client.get_waiter('resource_request_success').wait(RequestToken=response['ProgressEvent']['RequestToken'])
                    except botocore.exceptions.WaiterError as e:
                        self.module.fail_json_aws(e, msg='An error occurred waiting for the resource request to become successful.')
                result["changed"] = True
                result["result"] = response
            except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
                self.module.fail_json_aws(e, msg="")
            
        return result
