from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


# extending group model with GroupDescription model
class GroupDescription(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField(max_length=260)

    def __str__(self):
        return self.description


# extending user model with Profile model
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='defaults/profile_pic_default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=260, null=True, blank=True)
    twitter = models.URLField(max_length=150, null=True, blank=True)
    instagram = models.URLField(max_length=150, null=True, blank=True)
    facebook = models.URLField(max_length=150, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        img = img.resize((200, 200))
        img.save(self.profile_pic.path)


# Signal
# create profile when new user added
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
