# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ConfigParser
import ast
import os
from resource_management.core.resources.system import Execute

scriptDir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(scriptDir, 'download.ini')))

trinoTarUrl = config.get('download', 'trino_tar_url')
trinoTarName = trinoTarUrl.split('/')[-1]
trinoCliUrl = config.get('download', 'trino_cli_url')
jdk11Url = config.get('download', 'jdk11_url')
jdk11TarName = jdk11Url.split('/')[-1]

packageDir = os.path.dirname(scriptDir)
serviceDir = os.path.dirname(packageDir)
serviceName = os.path.basename(serviceDir)

trinoHome = '/data/trino/' + serviceName
jdk11Home = '/data/jdk11/'
etcDir = trinoHome + '/etc'
catalogDir = etcDir + '/catalog'
launcherPath = trinoHome + '/bin/launcher'

exportJavaHomeAndPath = ' export JAVA_HOME=' + jdk11Home + ' && export PATH=${JAVA_HOME}/bin:$PATH '


def create_connectors(connectors_to_add):
    if not connectors_to_add:
        return
    connectors_dict = ast.literal_eval(connectors_to_add)
    for connector in connectors_dict:
        connector_file = os.path.join(catalogDir, connector + '.properties')
        with open(connector_file, 'w') as f:
            for lineitem in connectors_dict[connector]:
                f.write('{0}\n'.format(lineitem))


def delete_connectors(connectors_to_delete):
    if not connectors_to_delete:
        return
    connectors_list = ast.literal_eval(connectors_to_delete)
    for connector in connectors_list:
        connector_file_name = os.path.join(catalogDir, connector + '.properties')
        Execute('rm -f {0}'.format(connector_file_name))
