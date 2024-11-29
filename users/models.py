from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('OPERATOR', 'operator'),
        ('SELLER', 'seller'),
        ('ADMIN', 'admin'),
    ]

    mobile = models.CharField(
        _("mobile"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required Field. Mobile without +98 , Example:09372222222"
        ),
        error_messages={
            "unique": _("A user with that mobile already exists."),
        },
    )
    # TODO: add mobile validator

    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    user_type =models.CharField(max_length=20, choices=USER_TYPES)

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
