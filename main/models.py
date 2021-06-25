from django.db import models
from tgbot.models import User
import uuid


class PageInfo(models.Model):
    name = models.CharField(max_length=120)
    # todo - split in 3 parts
    uuid = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)

    # TODO: not use charfield for this
    date_of_birth = models.CharField(max_length=20)

    first_two_passport_numbers = models.CharField(max_length=2)
    last_three_passport_numbers = models.CharField(max_length=3, default=None, null=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, default=None, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.creator is None:
            return 'tf this one doesnt have a creator'
        return f'PageInfo - [{self.name if self.name is not "" else "В процессе"}], ' \
               f'[{self.creator.username if self.creator.username is not None else self.creator.user_id}]'
