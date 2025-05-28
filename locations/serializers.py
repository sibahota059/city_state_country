from rest_framework import serializers
from .models import Country, State, City


class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    country_name = serializers.CharField(source='state.country.name', read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'state_id', 'state_name', 'country_name']


class StateSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    cities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = State
        fields = ['id', 'name', 'country_id', 'country_name', 'cities_count']
    
    def get_cities_count(self, obj):
        return obj.cities.count()


class StateWithCitiesSerializer(StateSerializer):
    cities = CitySerializer(many=True, read_only=True)
    
    class Meta(StateSerializer.Meta):
        fields = StateSerializer.Meta.fields + ['cities']


class CountrySerializer(serializers.ModelSerializer):
    states_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'shortname', 'phonecode', 'states_count']
    
    def get_states_count(self, obj):
        return obj.states.count()


class CountryWithStatesSerializer(CountrySerializer):
    states = StateSerializer(many=True, read_only=True)
    
    class Meta(CountrySerializer.Meta):
        fields = CountrySerializer.Meta.fields + ['states']


class CountryDetailSerializer(CountrySerializer):
    states = StateWithCitiesSerializer(many=True, read_only=True)
    
    class Meta(CountrySerializer.Meta):
        fields = CountrySerializer.Meta.fields + ['states']