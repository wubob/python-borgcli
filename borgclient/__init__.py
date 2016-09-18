# Copyright (c) 2016 Dataman Cloud
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging


from borgclient.client import HTTPClient
from borgclient.app import AppMixin
from borgclient.logs import LogMixin
from borgclient.metrics import MetricsMixin
from borgclient.user import UserMixin
from borgclient.auth import AuthMixin

from borgclient.exceptions import BorgException

_DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)8s [%(name)s] %(message)s"
_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


LOG = logging.getLogger(__name__)

_handler = logging.FileHandler("/var/log/borg-client.log")
_handler.setFormatter(
    logging.Formatter(fmt=_DEFAULT_LOG_FORMAT,
                      datefmt=_DEFAULT_LOG_DATE_FORMAT))

LOG.addHandler(_handler)
LOG.setLevel(logging.INFO)


class BorgClient(AppMixin, LogMixin, MetricsMixin, UserMixin, AuthMixin):
    """
    Client for user to use Borgsphere.
    """

    def __init__(self, server_url, email, password, token=None):

        self.server_url = server_url

        self.http = HTTPClient(server_url, email, password, token=token)

        super(BorgClient, self).__init__()

    @staticmethod
    def process_data(resp):
        """Processing data response from Borgsphere API."""
        try:
            LOG.info(resp.json) 
            return resp.json()
        except ValueError:
            LOG.info(resp.json) 
            return resp.status_code