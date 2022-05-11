from email import message
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from chat.managers import ThreadManager

# Create your models here.


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(models.Model):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=1200, null=True, blank=True)
    thread_type = models.CharField(
        max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField('auth.user')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count == 2:
            return f'{self.users.first()} and {self.users.last()}'
        else:
            return f'{self.name}'


class Messages(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    # receiver = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message
