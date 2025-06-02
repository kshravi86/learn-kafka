from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Bus
import decimal

class BusCRUDTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bus = Bus.objects.create(
            bus_name="Test Bus 1",
            source="City A",
            destination="City B",
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timezone.timedelta(hours=2),
            price=decimal.Decimal("25.00")
        )

    def test_bus_creation(self):
        initial_bus_count = Bus.objects.count()
        # Sane default for departure and arrival times, using strftime to format them as expected by the form
        departure_time_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        arrival_time_str = (timezone.now() + timezone.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

        response = self.client.post(reverse('bus_create'), {
            'bus_name': 'New Bus',
            'source': 'City C',
            'destination': 'City D',
            'departure_time': departure_time_str,
            'arrival_time': arrival_time_str,
            'price': '30.00'
        })
        self.assertEqual(response.status_code, 302) # Should redirect after creation
        self.assertEqual(Bus.objects.count(), initial_bus_count + 1)
        new_bus = Bus.objects.latest('id')
        self.assertEqual(new_bus.bus_name, 'New Bus')

    def test_bus_list_view(self):
        response = self.client.get(reverse('bus_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bus.bus_name)
        self.assertTemplateUsed(response, 'ticketing/bus_list.html')

    def test_bus_detail_view(self):
        response = self.client.get(reverse('bus_detail', args=[self.bus.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.bus.bus_name)
        self.assertContains(response, self.bus.source)
        self.assertTemplateUsed(response, 'ticketing/bus_detail.html')

    def test_bus_update_view(self):
        updated_name = "Updated Test Bus"
        # Sane default for departure and arrival times, using strftime to format them
        departure_time_str = self.bus.departure_time.strftime('%Y-%m-%d %H:%M:%S')
        arrival_time_str = self.bus.arrival_time.strftime('%Y-%m-%d %H:%M:%S')

        response = self.client.post(reverse('bus_update', args=[self.bus.pk]), {
            'bus_name': updated_name,
            'source': self.bus.source,
            'destination': self.bus.destination,
            'departure_time': departure_time_str,
            'arrival_time': arrival_time_str,
            'price': str(self.bus.price)
        })
        self.assertEqual(response.status_code, 302) # Should redirect after update
        self.bus.refresh_from_db()
        self.assertEqual(self.bus.bus_name, updated_name)

    def test_bus_delete_view(self):
        initial_bus_count = Bus.objects.count()
        response = self.client.post(reverse('bus_delete', args=[self.bus.pk]))
        self.assertEqual(response.status_code, 302) # Should redirect after delete
        self.assertEqual(Bus.objects.count(), initial_bus_count - 1)
