from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )
    location = models.PointField(
        blank=True,
        null=True,
        default=None)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Amenity(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    cuisine = models.CharField(max_length=255, null=True)
    location = models.PointField(
        blank=True,
        null=True,
        default=None)
    building = models.PolygonField(srid=4326, null=True, default=None)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    description = models.TextField()
    store = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    def __str__(self):
        return self.rating, self.description, self.store.name
