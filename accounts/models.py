from django.db import models

from django.contrib import admin

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=150, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Marilogger(models.Model):
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    action_username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return u"%s %s" % (self.date, self.message)

class MariloggerAdmin(admin.ModelAdmin):
    list_display = ('date', 'message', 'action_username',)
    search_fields = ('message',)

admin.site.register(Marilogger, MariloggerAdmin)