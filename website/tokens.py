from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#this class is used to create the token needed when creating the account activation url.
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()
