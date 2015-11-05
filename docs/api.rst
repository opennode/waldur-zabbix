Zabbix services list
----------------------

To get a list of services, run GET against **/api/zabbix/** as authenticated user.


Create a Zabbix service
-------------------------

To create a new Zabbix service, issue a POST with service details to **/api/zabbix/** as a customer owner.

Request parameters:

 - name - service name,
 - customer - URL of service customer,
 - settings - URL of Zabbix settings, if not defined - new settings will be created from server parameters,
 - dummy - is service dummy,

The following rules for generation of the service settings are used:

 - backend_url - Zabbix API URL;
 - username - zabbix user username (e.g. User);
 - password - zabbix user password (e.g. Password);
 - group_name - Zabbix group name for registered hosts (default: "nodeconductor");
 - interface_parameters - Parameters for hosts interface. (default: {"dns": "", "ip": "0.0.0.0", "main": 1,
                          "port": "10050", "type": 1, "useip": 1});
 - templates_names - List of zabbix hosts templates. (default: ["nodeconductor"]);


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
        "backend_url": "http://example.com/",
        "username": "User",
        "password": "Password",
    }


Link service to a project
-------------------------
In order to be able to provision Zabbix resources, it must first be linked to a project. To do that,
POST a connection between project and a service to **/api/zabbix-service-project-link/** as staff user or customer
owner.
For example,

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
To get a list of connections between a project and an oracle service, run GET against
**/api/zabbix-service-project-link/** as authenticated user. Note that a user can only see connections of a project
where a user has a role.


Create a new Zabbix resource (host)
-----------------------------------
A new Zabbix resource (host) can be created by users with project administrator role, customer owner role or with
staff privilege (is_staff=True). To create a host, client must issue POST request to **/api/zabbix-hosts/** with
parameters:

 - name - host name;
 - description - host description (optional);
 - link to the service-project-link object;


 Example of a valid request:

.. code-block:: http

    POST /api/zabbix-hosts/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "name": "test host",
        "description": "sample description",
        "service_project_link": "http://example.com/api/zabbix-service-project-link/1/",
    }


Host display
-----------

To get host data - issue GET request against **/api/zabbix-hosts/<host_uuid>/**.

Example rendering of the host object:

.. code-block:: javascript

    [
        {
            "url": "http://example.com/api/zabbix-hosts/5c28da08c93a40b391871f0900905ddc/",
            "uuid": "5c28da08c93a40b391871f0900905ddc",
            "name": "pavel-test-zabbix-15",
            "description": "",
            "start_time": null,
            "service": "http://example.com/api/zabbix/0923177a994742dd97257d004d3afae3/",
            "service_name": "Oman Zabbix service",
            "service_uuid": "0923177a994742dd97257d004d3afae3",
            "project": "http://example.com/api/projects/873d6858eabb4ec6b232b32da81d752a/",
            "project_name": "Oman Zabbix project",
            "project_uuid": "873d6858eabb4ec6b232b32da81d752a",
            "customer": "http://example.com/api/customers/01d40fb2ea154935915e46e83b73c7f4/",
            "customer_name": "Oman Zabbix customer",
            "customer_native_name": "",
            "customer_abbreviation": "",
            "project_groups": [],
            "resource_type": "Zabbix.Host",
            "state": "Online",
            "created": "2015-11-05T08:07:04.592Z"
        }
    ]


Delete host
----------

To delete host - issue DELETE request against **/api/zabbix-hosts/<host_uuid>/**.
