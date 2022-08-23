# Copyright: (c) 2022, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy

try:
    import botocore.waiter as core_waiter
except ImportError:
    pass  # caught by HAS_BOTO3

from ansible_collections.amazon.aws.plugins.module_utils.modules import (
    _RetryingBotoClientWrapper,
)


cloudcontrolapi_data = {
    "version": 2,
    "waiters": {
        "ResourceRequestSuccess": {
            "description": "Wait until resource operation request is successful",
            "delay": 5,
            "maxAttempts": 24,
            "operation": "GetResourceRequestStatus",
            "acceptors": [
                {
                    "matcher": "path",
                    "argument": "ProgressEvent.OperationStatus",
                    "state": "success",
                    "expected": "SUCCESS",
                },
                {
                    "matcher": "path",
                    "argument": "ProgressEvent.OperationStatus",
                    "state": "failure",
                    "expected": "FAILED",
                },
                {
                    "matcher": "path",
                    "argument": "ProgressEvent.OperationStatus",
                    "state": "success",
                    "expected": "CANCEL_COMPLETE",
                },
            ],
        }
    },
}


def _inject_limit_retries(model):

    extra_retries = [
        "RequestLimitExceeded",
        "Unavailable",
        "ServiceUnavailable",
        "InternalFailure",
        "InternalError",
        "TooManyRequestsException",
        "Throttling",
    ]

    acceptors = []
    for error in extra_retries:
        acceptors.append({"state": "success", "matcher": "error", "expected": error})

    _model = copy.deepcopy(model)

    for waiter in model["waiters"]:
        _model["waiters"][waiter]["acceptors"].extend(acceptors)

    return _model


def cloudcontrolapi_model(name):
    cloudcontrolapi_models = core_waiter.WaiterModel(
        waiter_config=_inject_limit_retries(cloudcontrolapi_data)
    )
    return cloudcontrolapi_models.get_waiter(name)


waiters_by_name = {
    (
        "CloudControlApi",
        "resource_request_success",
    ): lambda cloudcontrol: core_waiter.Waiter(
        "resource_request_success",
        cloudcontrolapi_model("ResourceRequestSuccess"),
        core_waiter.NormalizedOperationMethod(cloudcontrol.get_resource_request_status),
    ),
}


def get_waiter(client, waiter_name):
    if isinstance(client, _RetryingBotoClientWrapper):
        return get_waiter(client.client, waiter_name)
    try:
        return waiters_by_name[(client.__class__.__name__, waiter_name)](client)
    except KeyError:
        raise NotImplementedError(
            "Waiter {0} could not be found for client {1}. Available waiters: {2}".format(
                waiter_name,
                type(client),
                ", ".join(repr(k) for k in waiters_by_name.keys()),
            )
        )
