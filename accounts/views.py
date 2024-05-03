from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer  # You'll need to create this serializer
from django.contrib.auth import authenticate, login, logout
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import permission_classes
# from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from core.decorators import standardize_api_response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log in the user after successful registration
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    # @standardize_api_response
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                'detail': 'Login successful',
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    # @standardize_api_response
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'})


def check_session(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'username': request.user.username
        })
    else:
        return JsonResponse({'isAuthenticated': False}, status=401)

#
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#
#
#