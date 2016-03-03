import datetime
from dateutil.relativedelta import relativedelta
import unittest

from rest_framework import status, test

from nodeconductor.core.utils import datetime_to_timestamp
from nodeconductor.monitoring.utils import format_period
from nodeconductor.structure.tests import factories as structure_factories

from . import factories
from .. import models


class SlaTest(test.APITransactionTestCase):
    def setUp(self):
        self.staff = structure_factories.UserFactory(is_staff=True)
        self.client.force_authenticate(self.staff)
        self.itservice = factories.ITServiceFactory()

        today = datetime.date.today()
        period = format_period(today)
        self.timestamp = datetime_to_timestamp(today)

        next_month = datetime.date.today() + relativedelta(months=1)
        self.next_month = format_period(next_month)

        self.history = models.SlaHistory.objects.create(
            itservice=self.itservice, period=period, value=100.0)
        self.events = models.SlaHistoryEvent.objects.create(
            history=self.history, timestamp=self.timestamp, state='U')

    @unittest.skip('Should be fixed in NC-1192')
    def test_render_actual_sla(self):
        url = factories.ITServiceFactory.get_url(self.itservice)
        response = self.client.get(url)
        self.assertEqual(100.0, response.data['actual_sla'])

    def test_render_sla_events(self):
        url = factories.ITServiceFactory.get_events_url(self.itservice)
        response = self.client.get(url)
        self.assertEqual([{'timestamp': self.timestamp, 'state': 'U'}], response.data)

    def test_sla_is_not_available(self):
        url = factories.ITServiceFactory.get_url(self.itservice)
        response = self.client.get(url, data={'period': self.next_month})
        self.assertEqual(None, response.data['actual_sla'])

    def test_future_sla_events(self):
        url = factories.ITServiceFactory.get_events_url(self.itservice)
        response = self.client.get(url, data={'period': self.next_month})
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
