from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from datetime import date
from django.db import models
from django.db.models.signals import post_save

# Create your models here.
STATUS = (
    ('S', 'Student'),
    ('T', 'Tutor')
)

LEVELS = (
    ('G1', '1st Grade'),
    ('G2', '2nd Grade'),
    ('G3', '3rd Grade'),
    ('G4', '4th Grade'),
    ('G5', '5th Grade'),
    ('G6', '6th Grade'),
    ('G7', '7th Grade'),
    ('G8', '8th Grade'),
    ('G9', '9th Grade'),
    ('G10', '10th Grade'),
    ('G11', '11th Grade'),
    ('G12', '12th Grade'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=STATUS
    )

    # Add Avatar here or in a seperate model????----
    # avatar = models.ImageField(default)
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
    def __str__(self):
        return f"{self.user} is a {self.status}"


    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'profile_id': self.id})

class Task(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    field = models.CharField(max_length=20)
    level = models.CharField(
        max_length=3,
        choices=LEVELS,
        default=LEVELS[0][0]
    )
    body = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)

    # doc = ?? How to implement the pictures
    def __str__(self):
        return f'''
    Task_id: {self.id},
    Task Title: {self.title},
    Author: {self.author},
    Task Level: {self.get_level_display()},
    Field: {self.field},
    Body: {self.body}
    '''

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    body = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    # doc = ?? How to implement the pictures

    def __str__(self):
        return f'''
    comment_id: {self.id},
    Author: {self.author},
    In answer to the task_id: {self.task_id},
    Body: {self.body}
    '''

class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reciever")
    body = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    # doc = ?? How to implement the pictures

    def __str__(self):
        return f'''
    Message_id: {self.id},
    Sender: {self.sender},
    Reciever: {self.reciever},
    Body: {self.body},
    Created @: {self.date_created}
    '''

class Profile_Avatar(models.Model):
    url = models.CharField(max_length=200, default='https://i.imgur.com/qx38J6i.png')  # <- need to set default
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"This is the photo for profile_id: {self.profile_id} @{self.url}"

class Task_Doc(models.Model):
    url = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"This is the photo for task_id: {self.task_id} @{self.url}"

class Comment_Doc(models.Model):
    url = models.CharField(max_length=200)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"This is the photo for comment_id: {self.comment_id} @{self.url}"

class Message_Doc(models.Model):
    url = models.CharField(max_length=200)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return f"This is the photo for message_id: {self.message_id} @{self.url}"