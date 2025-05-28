# Placeholder for views.py
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Country, State, City
from .serializers import (
    CountrySerializer, CountryWithStatesSerializer, CountryDetailSerializer,
    StateSerializer, StateWithCitiesSerializer, CitySerializer
)
from .validators import validate_country_id, validate_state_id
from .pagination import StandardResultsSetPagination


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for countries.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'shortname']
    search_fields = ['name', 'shortname']
    ordering_fields = ['id', 'name', 'shortname']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountryWithStatesSerializer
        return CountrySerializer
    
    @action(detail=True, methods=['get'])
    def full_details(self, request, pk=None):
        """Get country with all states and cities."""
        try:
            country = self.get_object()
            serializer = CountryDetailSerializer(country)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search countries by name."""
        name = request.query_params.get('name', '')
        if not name:
            return Response(
                {'error': 'Name parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        countries = Country.objects.filter(name__icontains=name)
        page = self.paginate_queryset(countries)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for states.
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'country_id']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StateWithCitiesSerializer
        return StateSerializer
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Get states by country ID."""
        country_id = request.query_params.get('country_id')
        if not country_id:
            return Response(
                {'error': 'country_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = validate_country_id(country_id)
            states = State.objects.filter(country=country)
            page = self.paginate_queryset(states)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(states, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search states by name."""
        name = request.query_params.get('name', '')
        country_id = request.query_params.get('country_id')
        
        if not name:
            return Response(
                {'error': 'Name parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        states_query = Q(name__icontains=name)
        if country_id:
            try:
                validate_country_id(country_id)
                states_query &= Q(country_id=country_id)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        states = State.objects.filter(states_query)
        page = self.paginate_queryset(states)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(states, many=True)
        return Response(serializer.data)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for cities.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'name', 'state_id']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    
    @action(detail=False, methods=['get'])
    def by_state(self, request):
        """Get cities by state ID."""
        state_id = request.query_params.get('state_id')
        country_id = request.query_params.get('country_id')
        
        if not state_id:
            return Response(
                {'error': 'state_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            state = validate_state_id(state_id, country_id)
            cities = City.objects.filter(state=state)
            page = self.paginate_queryset(cities)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(cities, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Get cities by country ID."""
        country_id = request.query_params.get('country_id')
        
        if not country_id:
            return Response(
                {'error': 'country_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            country = validate_country_id(country_id)
            cities = City.objects.filter(state__country=country)
            page = self.paginate_queryset(cities)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(cities, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search cities by name with optional state and country filters."""
        name = request.query_params.get('name', '')
        state_id = request.query_params.get('state_id')
        country_id = request.query_params.get('country_id')
        
        if not name:
            return Response(
                {'error': 'Name parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cities_query = Q(name__icontains=name)
        
        if state_id:
            try:
                validate_state_id(state_id, country_id)
                cities_query &= Q(state_id=state_id)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif country_id:
            try:
                validate_country_id(country_id)
                cities_query &= Q(state__country_id=country_id)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        cities = City.objects.filter(cities_query)
        page = self.paginate_queryset(cities)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)


class GlobalSearchViewSet(viewsets.ViewSet):
    """
    API endpoint for global search across countries, states, and cities.
    """
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Global search across countries, states, and cities.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({
                'countries': [],
                'states': [],
                'cities': []
            })
        
        # Search in countries
        countries = Country.objects.filter(
            Q(name__icontains=query) | Q(shortname__icontains=query)
        )[:10]
        
        # Search in states
        states = State.objects.filter(name__icontains=query)[:10]
        
        # Search in cities
        cities = City.objects.filter(name__icontains=query)[:10]
        
        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'states': StateSerializer(states, many=True).data,
            'cities': CitySerializer(cities, many=True).data
        })