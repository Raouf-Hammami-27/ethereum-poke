from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from smartContract import settings
from rest_framework.authtoken.models import Token

import datetime
import pytz


class BearerAuthentication(TokenAuthentication):
        keyword = 'Bearer'

        def authenticate_credentials(self, key):
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            model = self.get_model()

            try:
                token = model.objects.select_related('user').get(key=key)
                token.created = token.created.replace(tzinfo=pytz.utc)
                user = token.user

            except model.DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid token')

            if not token.user.is_active:
                raise exceptions.AuthenticationFailed('User inactive or deleted')

            if token.created < utc_now - settings.TOKEN_EXPIRE_TIME:
                token.delete()
                token = Token.objects.create(user=user)
                token.created = datetime.datetime.now(tz=pytz.utc)
                token.save()
                raise exceptions.AuthenticationFailed('Token has expired')
            return (token.user, token)

