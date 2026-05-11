from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserRegistrationSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer