# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from backend.models import SoftwareConfiguration
from backend.serializers import SoftwareConfigurationSerializer


class PushAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response("Successfully called Push")


class PullAPIView(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response("Successfully called Pull")


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
                    "msg": "Invalid query or parameters"
                }, status=400)

        return Response(
            {
                "msg": "No parameters or queries provided"
            }, status=400)
