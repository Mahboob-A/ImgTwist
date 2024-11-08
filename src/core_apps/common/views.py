from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class HealthCheck(APIView):
    "API for Healthcheck of Img Twist Backend."

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Healthcheck for Img Twist Backend"""

        return Response({"status": "OK"}, HTTP_200_OK)
