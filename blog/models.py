from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Blog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField(blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    category=models.CharField(max_length=50,blank=True)

    pic = models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(blank=True)
    anonymous=models.BooleanField(default=False)

    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=50,blank=True)
    # region=models.CharField(max_length=50,blank=True)
    # 원하는거 아무거나 넣으면 됨

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# 자동으로 생성,저장