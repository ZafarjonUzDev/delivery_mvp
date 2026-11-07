from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Initial swappable user; customer authentication is a later task."""

    pass
