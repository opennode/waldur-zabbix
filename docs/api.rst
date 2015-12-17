Zabbix services list
--------------------

To get a list of services, run GET against **/api/zabbix/** as authenticated user.


Create a Zabbix service
-----------------------

To create a new Zabbix service, issue a POST with service details to **/api/zabbix/** as a customer owner.

Request parameters:

 - name - service name,
 - customer - URL of service customer,
 - settings - URL of Zabbix settings, if not defined - new settings will be created from server parameters,
 - dummy - is service dummy.

The following rules for generation of the service settings are used:

 - backend_url - Zabbix API URL (e.g. http://example.com/zabbix/api_jsonrpc.php);
 - username - Zabbix user username (e.g. admin);
 - password - Zabbix user password (e.g. zabbix);
 - host_group_name - Zabbix group name for registered hosts (default: "nodeconductor");
 - interface_parameters - default parameters for hosts interface. (default: {"dns": "", "ip": "0.0.0.0", "main": 1, "port": "10050", "type": 1, "useip": 1});
 - templates_names - List of Zabbix hosts templates. (default: ["NodeConductor"]);
 - database_parameters - Zabbix database parameters. (default: {"host": "localhost", "port": "3306", "name": "zabbix", "user": "admin", "password": ""})


Example of a request:


.. code-block:: http

    POST /api/zabbix/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "name": "My Zabbix"
        "customer": "http://example.com/api/customers/2aadad6a4b764661add14dfdda26b373/",
        "backend_url": "http://example.com/zabbix/api_jsonrpc.php",
        "username": "admin",
        "password": "zabbix"
    }


Link service to a project
-------------------------
In order to be able to provision Zabbix resources, it must first be linked to a project. To do that,
POST a connection between project and a service to **/api/zabbix-service-project-link/** as staff user or customer
owner. For example,

.. code-block:: http

    POST /api/zabbix-service-project-link/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "project": "http://example.com/api/projects/e5f973af2eb14d2d8c38d62bcbaccb33/",
        "service": "http://example.com/api/zabbix/b0e8a4cbd47c4f9ca01642b7ec033db4/"
    }

To remove a link, issue DELETE to url of the corresponding connection as staff user or customer owner.


Project-service connection list
-------------------------------
To get a list of connections between a project and a Zabbix service, run GET against
**/api/zabbix-service-project-link/** as authenticated user. Note that a user can only see connections of a project
where a user has a role.


Create a new Zabbix resource (host)
-----------------------------------
A new Zabbix resource (host) can be created by users with project administrator role, customer owner role or with
staff privilege (is_staff=True). To create a host, client must issue POST request to **/api/zabbix-hosts/** with
parameters:

 - name - host name;
 - service_project_link - url of service-project-link;
 - visible_name - host visible name (optional if scope is defined);
 - scope - optional url of related object, for example of OpenStack instance;
 - description - host description (optional);
 - interface_parameters - host interface parameters (optional, default value will be taken from service settings, if
   not specified);
 - host_group_name - host group name (optional, default value will be taken from service settings if not specified);
 - templates - list of template urls (optional, default value will be taken from service settings if not specified).


Example of a valid request:

.. code-block:: http

    POST /api/zabbix-hosts/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "name": "test host",
        "visible_name": "test host",
        "description": "sample description",
        "service_project_link": "http://example.com/api/zabbix-service-project-link/1/",
        "templates": [
            {
                "url": "http://example.com/api/zabbix-templates/99771937d38d41ceba3352b99e01b00b/"
            }
        ]
    }


Host display
------------

To get host data - issue GET request against **/api/zabbix-hosts/<host_uuid>/**.

Example rendering of the host object:

.. code-block:: javascript

    {
        "url": "http://example.com/api/zabbix-hosts/c2c29036f6e441908e5f7ca0f2441431/",
        "uuid": "c2c29036f6e441908e5f7ca0f2441431",
        "name": "a851fa75-5599-467b-be11-3d15858e8673",
        "description": "",
        "start_time": null,
        "service": "http://example.com/api/zabbix/1ffaa994d8424b6e9a512ad967ad428c/",
        "service_name": "My Zabbix",
        "service_uuid": "1ffaa994d8424b6e9a512ad967ad428c",
        "project": "http://example.com/api/projects/8dc8f34f27ef4a4f916184ab71e178e3/",
        "project_name": "Default",
        "project_uuid": "8dc8f34f27ef4a4f916184ab71e178e3",
        "customer": "http://example.com/api/customers/7313b71bd1cc421ea297dcb982e40260/",
        "customer_name": "Alice",
        "customer_native_name": "",
        "customer_abbreviation": "",
        "project_groups": [],
        "tags": [],
        "error_message": "",
        "resource_type": "Zabbix.Host",
        "state": "Online",
        "created": "2015-10-16T11:18:59.596Z",
        "backend_id": "2535",
        "visible_name": "a851fa75-5599-467b-be11-3d15858e8673",
        "interface_parameters": "{u'ip': u'0.0.0.0', u'useip': 1, u'dns': u'', u'main': 1, u'type': 1, u'port': u'10050'}",
        "host_group_name": "nodeconductor",
        "scope": null,
        "templates": [
            {
                "url": "http://example.com/api/zabbix-templates/99771937d38d41ceba3352b99e01b00b/",
                "uuid": "99771937d38d41ceba3352b99e01b00b",
                "name": "Template NodeConductor Instance",
                "items": [
                    "kvm.vm.cpu.num",
                    "kvm.vm.cpu.util",
                    "kvm.vm.disk.size",
                    "kvm.vm.memory.size",
                    "kvm.vm.memory.size.used",
                    "kvm.vm.memory.util",
                    "kvm.vm.memory_util",
                    "kvm.vm.status",
                    "openstack.instance.cpu.num",
                    "openstack.instance.cpu.util",
                    "openstack.instance.cpu_util",
                    "openstack.instance.disk.ephemeral.size",
                    "openstack.instance.disk.read.bytes",
                    "openstack.instance.disk.read.requests",
                    "openstack.instance.disk.root.size",
                    "openstack.instance.disk.size",
                    "openstack.instance.disk.write.bytes",
                    "openstack.instance.disk.write.requests",
                    "openstack.instance.memory",
                    "openstack.instance.network.incoming.bytes",
                    "openstack.instance.network.incoming.packets",
                    "openstack.instance.network.outgoing.bytes",
                    "openstack.instance.network.outgoing.packets",
                    "openstack.instance.status",
                    "openstack.instance.vcpus",
                    "openstack.vm.disk.size"
                ]
            }
        ]
    }


Delete host
-----------

To delete host - issue DELETE request against **/api/zabbix-hosts/<host_uuid>/**.


Host statistics
----------------

URL: **/api/zabbix-hosts/<host_uuid>/items_history/**

Request should specify datetime points and items. There are two ways to define datetime points for historical data.

1. Send *?point=<timestamp>* parameter that can list. Response will contain historical data for each given point in the
   same order.
2. Send *?start=<timestamp>*, *?end=<timestamp>*, *?points_count=<integer>* parameters.
   Result will contain <points_count> points from <start> to <end>.

Also you should specify one or more name of host template items, for example 'openstack.instance.cpu_util'

Response is list of datapoint, each of which is dictionary with following fields:
 - 'point' - timestamp;
 - 'value' - values are converted from bytes to megabytes, if possible;
 - 'item' - name of host template item.

Example response:

.. code-block:: javascript

    [
        {
            "point": 1441935000,
            "value": 0.1393,
            "item": "openstack.instance.cpu_util"
        },
        {
            "point": 1442163600,
            "value": 10.2583,
            "item": "openstack.instance.cpu_util"
        },
        {
            "point": 1442392200,
            "value": 20.3725,
            "item": "openstack.instance.cpu_util"
        },
        {
            "point": 1442620800,
            "value": 30.3426,
            "item": "openstack.instance.cpu_util"
        },
        {
            "point": 1442849400,
            "value": 40.3353,
            "item": "openstack.instance.cpu_util"
        },
        {
            "point": 1443078000,
            "value": 50.3574,
            "item": "openstack.instance.cpu_util"
        }
    ]


Aggregated host statistics
--------------------------

URL: **/api/zabbix-hosts/aggregated_items_history/**

Request should specify host filtering parameters, datetime points, and items.
Host filtering parameters are the same as for */api/resources/* endpoint.
Input/output format is the same as for **/api/zabbix-hosts/<host_uuid>/items_history/** endpoint.
