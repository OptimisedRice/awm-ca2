from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from psycopg2.extensions import JSON

from .serializers import ReviewSerializer
from . import models
# Create your views here.


def update_location(request):
    try:
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User details")
        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)
        user_profile.location = point
        user_profile.save()
        return JsonResponse({"message": f"Set location to {point.wkt}."}, status=200)
    except Exception as e:
        return JsonResponse({"message": JSON.stringify(e)},status=400)


def review(request):
    try:
        print(request.POST["id"])
        reviews = models.Review.objects.filter(store__id=request.POST["id"])
        if not reviews:
            raise ValueError("Can't get Amenity reviews")
        return JsonResponse({"reviews": ReviewSerializer(reviews, many=True).data}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "error!"}, status=500)


def submit_review(request):
    try:
        review = models.Review(description=request.POST["description"],
                               rating=request.POST["rating"],
                               store_id=request.POST["store_id"])

        review.save()
        return JsonResponse({"message": "review submitted successfully."}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "error!"}, status=500)


def home(request):
    amenities = models.Amenity.objects.all().values
    return render(request, "home.html", {"amenities": amenities})
