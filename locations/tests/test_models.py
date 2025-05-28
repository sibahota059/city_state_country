from django.test import TestCase
from locations.models import Country, State, City


class CountryModelTest(TestCase):
    def setUp(self):
        Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )

    def test_country_creation(self):
        country = Country.objects.get(shortname="US")
        self.assertEqual(country.name, "United States")
        self.assertEqual(country.phonecode, 1)


class StateModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(
            shortname="US",
            name="United States",
            phonecode=1
        )
        State.objects.create(
            name="California",
            country=self.country
        )

    def test_state_creation(self):
        state = State.objects.get(name="California")
        self.assertEqual(state.country, self.country)


class CityModelTest(TestCase):
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
        City.objects.create(
            name="Los Angeles",
            state=self.state
        )

    def test_city_creation(self):
        city = City.objects.get(name="Los Angeles")
        self.assertEqual(city.state, self.state)
        self.assertEqual(city.state.country, self.country)