from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from products.models import Chapter


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapters = models.ManyToManyField(Chapter, blank=True)

    def __str__(self):
        return self.user.username


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = CustomerProfile.objects.get_or_create(user=instance)
    user_profile.save()

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)

