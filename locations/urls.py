from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, StateViewSet, CityViewSet, GlobalSearchViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'cities', CityViewSet)
router.register(r'global', GlobalSearchViewSet, basename='global')

urlpatterns = [
    path('', include(router.urls)),
    # Search endpoints
    path('search/', GlobalSearchViewSet.as_view({'get': 'search'}), name='global-search'),
]