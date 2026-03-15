from django.conf import settings
from django.db import models

from products.models import branch


class UserBranch(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_branch',
    )
    branch = models.ForeignKey(
        branch,
        on_delete=models.CASCADE,
        related_name='users',
    )

    def __str__(self):
        return f"{self.user.username} - {self.branch.name}"
