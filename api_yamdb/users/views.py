from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import UserIsAdmin
from .serializers import UserMeSerializer, UserSerializer


def check_required_fields(request, fields):
    error_required_fields = {}

    for field_name in fields:
        field_value = request.data.get(field_name)
        if not field_value:
            error_required_fields[field_name] = [
                'Missing field or empty value.'
            ]

    if error_required_fields:
        raise ValidationError(detail=error_required_fields)


class SignupViewSet(viewsets.ViewSet):
    def create(self, request):
        required_fields = ('username', 'email',)
        check_required_fields(request, required_fields)

        username = request.data.get('username')
        email = request.data.get('email')

        user = User.objects.filter(
            username=username, email=email
        )

        if user.exists():
            found_user = user[0]
            found_user.email_user(
                'Registration confirmation code from YAMDB',
                f'{found_user.confirmation_code}'
            )
            return Response(
                data={'username': username, 'email': email},
                status=status.HTTP_200_OK
            )

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.email_user(
                'Registration confirmation code from YAMDB',
                f'{user.confirmation_code}'
            )

        response_data = {'username': username, 'email': email}
        return Response(data=response_data, status=status.HTTP_200_OK)


class TokenViewSet(viewsets.ViewSet):
    def create(self, request):
        required_fields = ('username', 'confirmation_code',)
        check_required_fields(request, required_fields)

        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        user = get_object_or_404(
            User, username=username
        )

        if user.confirmation_code != confirmation_code:
            raise ValidationError(detail={
                'confirmation_code': ['Invalid confirmation code.']
            })

        token = AccessToken.for_user(user)
        return Response(
            data={'token': str(token)}, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (UserIsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False, methods=('GET', 'PATCH'),
            permission_classes=(permissions.IsAuthenticated,),
            serializer_class=UserMeSerializer)
    def me(self, request):
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
