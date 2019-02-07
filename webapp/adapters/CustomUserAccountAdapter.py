from allauth.account.adapter import DefaultAccountAdapter
from smartContract.settings import W3


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field
        username = request.data.get('username', '')
        address = W3.personal.newAccount(username)
        user = super().save_user(request, user, form, False)
        user_field(user, 'address', address)
        user.save()
        return user

