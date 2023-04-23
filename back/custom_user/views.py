from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, UserSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserView(ViewSet):
    queryset = User.objects.all()

    def list(self, request):

        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)
