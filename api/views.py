from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint providing links to all main endpoints.
    """
    return Response({
        'countries': reverse('country-list', request=request, format=format),
        'states': reverse('state-list', request=request, format=format),
        'cities': reverse('city-list', request=request, format=format),
        'global_search': reverse('global-search', request=request, format=format),
        'documentation': {
            'swagger': reverse('schema-swagger-ui', request=request, format=format),
            'redoc': reverse('schema-redoc', request=request, format=format)
        }
    })