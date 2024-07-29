from django.db import models
from account.models import User

# Create your models here.


GENDERSELECT=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    ]
class Genderselect(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genderselect = models.CharField(max_length=10,choices=GENDERSELECT,default='B')

    def __str__(self):
        return f"{self.genderselect}"


class Media(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/')
    timestamp = models.DateTimeField(auto_now_add=True)


class Friendconnection(models.Model):
    send_by = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    send_to = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date_friend = models.DateTimeField(auto_now_add=True)
    short_list = models.BooleanField(default=False)
    not_interest = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'From {self.sender.username} to {self.receiver.username} at {self.timestamp}'