import urllib

from mock import patch
from rest_framework import status, test

from nodeconductor.structure.tests import factories as structure_factories

from . import factories


@patch('nodeconductor.structure.models.ServiceSettings.get_backend')
class ServiceDeletionTest(test.APITransactionTestCase):
    def setUp(self):
        self.staff = structure_factories.UserFactory(is_staff=True)
        self.client.force_authenticate(self.staff)
        self.service = factories.ZabbixServiceFactory()
        self.url = factories.ZabbixServiceFactory.get_url(self.service, 'services')

    def test_service_ids_are_required(self, mock_backend):
        mock_backend().get_services.return_value = []
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(mock_backend().get_services.called)

    def test_when_services_are_deleted_api_calls_backend(self, mock_backend):
        mock_backend().get_services.return_value = [
            {'id': '1', 'name': 'Availability of 1'},
            {'id': '2', 'name': 'Availability of 2'},
            {'id': '3', 'name': 'Availability of 3'}
        ]

        service_ids = ['1', '2', '3']
        params = urllib.urlencode({'id': service_ids}, doseq=True)
        url = self.url + '?' + params
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual({'detail': 'Services 1, 2, 3 are deleted.'}, response.data)
        mock_backend().delete_services.assert_called_once_with(service_ids)
