Installation from source
------------------------

 * `Install NodeConductor <http://nodeconductor.readthedocs.org/en/latest/guide/intro.html#installation-from-source>`_
 * Clone NodeConductor Zabbix repository

  .. code-block:: bash

    git clone git@code.opennodecloud.com:nodeconductor/nodeconductor-zabbix.git

 * Install NodeConductor Zabbix into NodeConductor virtual environment

  .. code-block:: bash

    cd /path/to/zabbix/
    python setup.py install

Configuration
+++++++++++++

Zabbix plugin settings should be defined in NodeConductor's settings.py file.

For example,

.. code-block:: python

        NODECONDUCTOR_ZABBIX_SMS_SETTINGS = {
            'SMS_EMAIL_FROM': 'zabbix@example.com',
            'SMS_EMAIL_RCPT': '{phone}@example.com',
        }

Available settings:

.. glossary::

    NODECONDUCTOR_ZABBIX_SMS_SETTINGS
      A dictionary of configurations for Zabbix SMS notifications.

        SMS_EMAIL_FROM
            Defines the email from which SMS notification will be sent.

        SMS_EMAIL_RCPT
            Defines the email to which SMS notification will be sent.
            It should include `{phone}`string, which will be after replaced
            with a phone number.

NodeConductor also needs access to Zabbix database. For that a read-only user needs to be created in Zabbix database.

Zabbix database connection is configured as follows:

.. code-block:: python

    DATABASES = {
        'zabbix': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': 'zabbix_db_host',
            'NAME': 'zabbix_db_name',
            'PORT': 'zabbix_db_port',
            'USER': 'zabbix_db_user',
            'PASSWORD': 'zabbix_db_password',
        }
    }

.. glossary::

    zabbix_db_host
      Hostname of the Zabbix database.

    zabbix_db_port
      Port of the Zabbix database.

    zabbix_db_name
      Zabbix database name.

    zabbix_db_user
      User for connecting to Zabbix database.

    zabbix_db_password
      Password for connecting to Zabbix database.
