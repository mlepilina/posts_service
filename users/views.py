from rest_framework import generics, status, request
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(new_user.password)
        new_user.save()


class UserInfoView(APIView):

    def get(self, request: Request) -> Response:
        """Запрос на профиль пользователя"""

        user_id = request.query_params.get('user_id', 0)
        user = get_object_or_404(User, pk=user_id)

        response_data = {
            'id': user.pk,
            'email': user.email,
            'phone': user.phone,
            'birth_date': user.birth_date,
            'create_date': user.create_date,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

    def patch(self, request: Request):
        """Редактировать профиль пользователя"""

        user_id = request.query_params.get('user_id', 0)
        user = get_object_or_404(User, pk=user_id)
        if user == request.user or request.user.is_staff is True:
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                'login': user.email,
                'phone': user.phone,
                'birth_date': user.birth_date,
                'change_date': user.change_date,
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        return Response(data={'error': 'Нет прав для редактирования'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request):
        """Удалить пользователя"""
        user_id = request.query_params.get('user_id', 0)
        user = get_object_or_404(User, pk=user_id)
        if request.user.is_staff:
            user.delete()
            return Response(data={'Пользователь успешно удален.'}, status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'error': 'Профили пользователей могут удалять только администраторы.'},
            status=status.HTTP_400_BAD_REQUEST
        )

