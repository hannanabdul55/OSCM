from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from backend.models import SoftwareConfiguration
from backend.serializers import SoftwareConfigurationSerializer


# Utility functions
def get_db_os_version(value_object):
    def get_db_os_for(this_value):
        if 'darwin' in this_value.lower():
            return SoftwareConfiguration.OS_MAC
        elif 'linux' in this_value.lower():
            return SoftwareConfiguration.OS_LINUX

    if isinstance(value_object, list):
        returns = []
        for value in value_object:
            returns.append(get_db_os_for(value))
        return returns

    elif isinstance(value_object, str):
        return get_db_os_for(value_object)


# Create your views here.
class PutAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response("Successfully called Put API")


class GetAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        params = dict(request.query_params)
        for k, v in params.iteritems():
            params[k] = v[0] if isinstance(v, list) and len(v) == 1 else v
            if k == "os":
                params[k] = get_db_os_version(v)
        filters = {}
        for k, v in params.iteritems():
            if isinstance(v, list):
                filters['%s__in' % k] = v
            else:
                filters['%s__icontains' % k] = v
        soft_configs = SoftwareConfiguration.objects.filter(**filters)
        return Response(soft_configs)


class SearchAPIView(ListAPIView):
    serializer_class = SoftwareConfigurationSerializer

    def get(self, request, *args, **kwargs):
        tag = request.query_params.get('tag', None)
        if tag:
            try:
                soft_configs = SoftwareConfiguration.objects.filter(
                    tag__icontains=tag)
                return Response(soft_configs)
            except:
                return Response(
                {
                    "error": "Invalid query or parameters"
                }, status=400)

        return Response(
            {
                "error": "No parameters or queries provided"
            }, status=400)
