from django.contrib.gis import admin
from .models import Profile, Amenity
# Register your models here.
admin.site.register(Profile, admin.OSMGeoAdmin)
admin.site.register(Amenity, admin.OSMGeoAdmin)