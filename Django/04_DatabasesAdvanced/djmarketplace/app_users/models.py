from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(max_length=20, default=0, blank=True)
    purchases = models.IntegerField(max_length=20, default=0, blank=True)

    def statys(self):
        if self.purchases <= 20000:
            return 'Junior'
        elif self.purchases <= 50000:
            return 'Middle'
        elif self.purchases > 50000:
            return 'Senior'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
