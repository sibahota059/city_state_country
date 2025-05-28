from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from locations.models import Country, State, City


class CountryViewSetTest(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )
        self.country2 = Country.objects.create(
            shortname="CA",
            name="Canada",
            phonecode=1
        )

    def test_list_countries(self):
        url = reverse('country-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_countries(self):
        url = reverse('country-search')
        response = self.client.get(url, {'name': 'united'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'United States')


class StateViewSetTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )
        self.state1 = State.objects.create(
            name="California",
            country=self.country
        )
        self.state2 = State.objects.create(
            name="New York",
            country=self.country
        )

    def test_list_states(self):
        url = reverse('state-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_states_by_country(self):
        url = reverse('state-by-country')
        response = self.client.get(url, {'country_id': self.country.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_states(self):
        url = reverse('state-search')
        response = self.client.get(url, {'name': 'cal'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'California')


class CityViewSetTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )
        self.state = State.objects.create(
            name="California",
            country=self.country
        )
        self.city1 = City.objects.create(
            name="Los Angeles",
            state=self.state
        )
        self.city2 = City.objects.create(
            name="San Francisco",
            state=self.state
        )

    def test_list_cities(self):
        url = reverse('city-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_cities_by_state(self):
        url = reverse('city-by-state')
        response = self.client.get(url, {'state_id': self.state.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_cities_by_country(self):
        url = reverse('city-by-country')
        response = self.client.get(url, {'country_id': self.country.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_cities(self):
        url = reverse('city-search')
        response = self.client.get(url, {'name': 'los'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Los Angeles')


class GlobalSearchViewSetTest(APITestCase):
    def setUp(self):
        # Create test data for global search
        self.country = Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )
        self.state = State.objects.create(
            name="California",
            country=self.country
        )
        self.city = City.objects.create(
            name="Los Angeles",
            state=self.state
        )

    def test_global_search(self):
        url = reverse('global-search')
        response = self.client.get(url, {'q': 'united'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['countries']), 1)
        self.assertEqual(response.data['countries'][0]['name'], 'United States')

        # Test search with no results
        response = self.client.get(url, {'q': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['countries']), 0)
        self.assertEqual(len(response.data['states']), 0)
        self.assertEqual(len(response.data['cities']), 0)