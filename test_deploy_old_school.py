# Copyright (c) 2015 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import uuid

import config as cfg
import muranomanager as core

CONF = cfg.cfg.CONF


class MuranoOldSchoolTest(core.MuranoTestsCore):
    @classmethod
    def setUpClass(cls):
        super(MuranoOldSchoolTest, cls).setUpClass()

        cls.docker = CONF.murano.docker_image
        cls.flavor = CONF.murano.standard_flavor

    def setUp(self):
        super(MuranoOldSchoolTest, self).setUp()

        self.environments = []

    def tearDown(self):
        super(MuranoOldSchoolTest, self).tearDown()

        for env in self.environments:
            try:
                self.environment_delete(env)
            except Exception:
                pass

    def test_deploy_hdp(self):
        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "hdp-sandbox",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": self.rand_name("testMurano_hdp")
            },
            "name": self.rand_name("test_HDP-Sandbox"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "hdp-sandbox"
                },
                "type": "io.murano.apps.HDPSandbox",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 8888)

    # TODO: test fails when floating ip is assigned to both instances. Passes when assign it only to Apache instance.
    def test_deploy_apache_http_mysql_wordpress(self):
        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "Ubuntu 14.04 LTS x64 (pre installed murano agent)",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": self.rand_name("testMurano")
            },
            "name": self.rand_name("teMurano"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Apache"
                },
                "type": "io.murano.apps.apache.ApacheHttpServer",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.apache = self.create_service(environment, session, post_body)

        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "Ubuntu 14.04 LTS x64 (pre installed murano agent)",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": self.rand_name("testMurano")
            },
            "database": self.rand_name('db'),
            "username": self.rand_name('user'),
            "password": self.rand_name('P@s5'),
            "name": self.rand_name("teMurano"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "MySQL"
                },
                "type": "io.murano.databases.MySql",
                "id": str(uuid.uuid4())
            }
        }
        self.mysql = self.create_service(environment, session, post_body)

        post_body = {
            "name": self.rand_name('WP'),
            "server": self.apache,
            "database": self.mysql,
            "dbName": self.rand_name('wp'),
            "dbUser": self.rand_name('wpuser'),
            "dbPassword": self.rand_name('P@s5'),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "WordPress"
                },
                "type": "io.murano.apps.WordPress",
                "id": str(uuid.uuid4())
            }
        }
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 80)
        self.check_path(environment, "wordpress")

    def test_deploy_postgres(self):
        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "Ubuntu 14.04 LTS x64 (pre installed murano agent)",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": self.rand_name("testMurano")
            },
            "database": self.rand_name('db'),
            "username": self.rand_name('user'),
            "password": self.rand_name('P@s5'),
            "name": self.rand_name("teMurano"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "PostgreSQL"
                },
                "type": "io.murano.databases.PostgreSql",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 5432)

    def test_deploy_apache_tomcat(self):
        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "Ubuntu 14.04 LTS x64 (pre installed murano agent)",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": self.rand_name("testMurano")
            },
            "database": self.rand_name('db'),
            "username": self.rand_name('user'),
            "password": self.rand_name('P@s5'),
            "name": self.rand_name("teMurano"),
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Tomcat"
                },
                "type": "io.murano.apps.apache.Tomcat",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 8080)

    def test_deploy_zabbix_server(self):
        post_body = {
            "instance": {
                "flavor": self.flavor,
                "image":
                    "Ubuntu 14.04 LTS x64 (pre installed murano agent)",
                "assignFloatingIp": True,
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
                "name": "ZabbixServer"
            },
            "database": "zabbix",
            "username": "zabbix",
            "password": self.rand_name('P@s5'),
            "name": "ZabbixServer",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Zabbix Server"
                },
                "type": "io.murano.apps.ZabbixServer",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 80)
        self.check_path(environment, "zabbix")

    def test_deploy_standalone_docker(self):
        post_body = {
            "instance": {
                "name": self.rand_name("Docker"),
                "assignFloatingIp": True,
                "keyname": "",
                "flavor": self.flavor,
                "image":
                    "Ubuntu14.04 x64 (pre-installed murano agent and docker)",
                "?": {
                    "type": "io.murano.resources.LinuxMuranoInstance",
                    "id": str(uuid.uuid4())
                },
            },
            "name": "DockerVM",
            "?": {
                "_{id}".format(id=uuid.uuid4().hex): {
                    "name": "Docker VM Service"
                },
                "type": "io.murano.apps.docker.DockerSingleVMServer50",
                "id": str(uuid.uuid4())
            }
        }
        environment = self.create_env()
        session = self.create_session(environment)
        self.create_service(environment, session, post_body)
        self.deploy_environment(environment, session)
        self.deployment_success_check(environment, 22, 2375)