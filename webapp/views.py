from webapp.repositories import  TransactionRepository as Transaction
from rest_auth.views import LoginView,create_token,jwt_encode,LogoutView
from rest_framework import status
from smartContract.settings import W3,TOKEN_EXPIRE_TIME
from rest_framework.response import Response
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (
    logout as django_logout
)


class TransactionList(Transaction.TransactionList):
    pass


class Login(LoginView):

    def login(self):

        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

        print(" status of unlock", self.user.address, self.user.username)

        st = W3.personal.unlockAccount(self.user.address, self.user.username, int(TOKEN_EXPIRE_TIME.total_seconds()))

        print(" status of unlock", st)


class Logout(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            W3.personal.lockAccount(self.user.address)
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)