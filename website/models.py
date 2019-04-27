from django.db import models
from  django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=20)

    def __self(self):
        return self.user.username

'''
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()'''

def email_new_user(sender, **kwargs):
    if kwargs["created"]:  # only for new users
        new_user = kwargs["instance"]
        print(new_user.email)
        send_mail('Hello From EBook.com', 'Hello there.. Your account is created but not active yet!! Please wait for minimum 30 minutes', 'sandip.kar@iiitb.org',[new_user.email], fail_silently=False)
        send_mail('Hello From EBook.com', new_user.username+' is newly created account!',
                  'sandip.kar@iiitb.org', ['sandipkar.asn@gmail.com'], fail_silently=False)

post_save.connect(email_new_user, sender=User)