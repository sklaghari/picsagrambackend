from djoser.constants import Messages
from django.utils.translation import gettext_lazy as _


class CustomMessages(Messages):
    INACTIVE_ACCOUNT_ERROR = _("Account with this email is not active. Please activate account.")