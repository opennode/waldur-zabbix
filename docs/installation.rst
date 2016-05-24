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

Zabbix plugin settings should be defined in NodeConductor's settings.py file
under **NODECONDUCTOR_ZABBIX** section.

For example,

.. code-block:: python

        NODECONDUCTOR_ZABBIX = {
            'SMS_SETTINGS': {
                'SMS_EMAIL_FROM': 'zabbix@example.com',
                'SMS_EMAIL_RCPT': '{phone}@example.com',
            },
        }

Available settings:

.. glossary::

    SMS_SETTINGS
      A dictionary of configurations for Zabbix SMS notifications.

        SMS_EMAIL_FROM
            Defines the email from which SMS notification will be sent.

        SMS_EMAIL_RCPT
            Defines the email to which SMS notification will be sent.
            It should include `{phone}` string, which will be after replaced
            with a phone number.
