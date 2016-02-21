from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from backend.models import SoftwareConfiguration
from backend.serializers import SoftwareConfigurationSerializer


# Utility functions
def humanize_os(val):
    return SoftwareConfiguration.OS_CHOICES[int(val)][1][3:].lower()


def get_db_os_version(value_object):
    def get_db_os_for(this_value):
        if 'darwin' in str(this_value).lower():
            return SoftwareConfiguration.OS_DARWIN
        elif 'linux' in str(this_value).lower():
            return SoftwareConfiguration.OS_LINUX

    if isinstance(value_object, list):
        returns = []
        for value in value_object:
            returns.append(get_db_os_for(value))
        return returns

    else:
        return get_db_os_for(value_object)


def serialize_soft_configs(queryset):
    serializer = SoftwareConfigurationSerializer(queryset, many=True)
    return serializer.data


# Create your views here.
class PutAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        allowed_keys = ["os", "arch", "name", "version", "command", "tag", "url"]
        essential_keys = ["os", "arch", "name", "version"]
        params = dict(request.query_params)
        essentials = {}
        for k, v in params.items():
            if k in allowed_keys:
                params[k] = v[0] if isinstance(v, list) and len(v) == 1 else v
                if k == "os":
                    params[k] = get_db_os_version(params[k])
                if k in essential_keys:
                    essentials[k] = params[k]
            else:
                del params[k]
        try:
            soft_configs = SoftwareConfiguration.objects.filter(**essentials)
            if soft_configs.count() > 0:
                for soft_config in soft_configs:
                    if "command" in params.keys():
                        soft_config.command = params["command"]
                    if "tag" in params.keys():
                        soft_config.tag = params["tag"]
                    if "url" in params.keys():
                        if params["url"]:
                            soft_config.tag = params["url"]
                            soft_config.save()
            else:
                SoftwareConfiguration.objects.create(**params)

            return Response({
                "message": "Successfully put. Fields populated: %s" % ", ".join(
                    params.keys())
            }, status=201)
        except:
            return Response({
                "error": "Invalid parameters provided"
            }, status=400)


class GetAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        allowed_keys = ["os", "arch", "name", "version"]
        params = dict(request.query_params)
        for k, v in params.items():
            if k in allowed_keys:
                params[k] = v[0] if isinstance(v, list) and len(v) == 1 else v
                if k == "os":
                    params[k] = get_db_os_version(params[k])
            else:
                del params[k]
        filters = {}
        for k, v in params.iteritems():
            if isinstance(v, list):
                filters['%s__in' % k] = v
            else:
                if "arch" in k:
                    filters['%s__in' % k] = [str(v), SoftwareConfiguration.ARCH_BOTH]
                filters['%s__icontains' % k] = v
        print filters
        soft_configs = SoftwareConfiguration.objects.filter(**filters)
        response = serialize_soft_configs(soft_configs)
        for index in range(len(response)):
            response[index]["os"] = humanize_os(response[index]["os"])
            print response[index]

        return Response(serialize_soft_configs(response))


class SearchAPIView(ListAPIView):
    serializer_class = SoftwareConfigurationSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        tag = request.query_params.get('tag', None)
        if tag:
            try:
                soft_configs = SoftwareConfiguration.objects.filter(
                    tag__icontains=tag)
                self.queryset = soft_configs
                return Response(serialize_soft_configs(soft_configs))
            except:
                return Response(
                    {
                        "error": "Invalid query or parameters"
                    }, status=400)

        return Response(
            {
                "error": "No parameters or queries provided"
            }, status=400)
