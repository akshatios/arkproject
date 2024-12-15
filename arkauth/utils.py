# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self,user,timestamp):
#         return str(user.pk)+ str(timestamp) + str(user.is_active)

# generate_token=TokenGenerator()


# utils.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active))

generate_token = TokenGenerator()
