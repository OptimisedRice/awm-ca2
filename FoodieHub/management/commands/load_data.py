from io import StringIO

from FoodieHub.models import Amenity
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from urllib.parse import quote
import geopandas as gpd
class Command(BaseCommand):
    help = 'load amenity data from OSM Overpass API'

    def handle(self, *args, **options):
        Amenity.objects.all().delete() # delete amenity data

        # with open("FoodieHub/data/restaurants.geojson") as f:
        #     gj = geojson.load(f)
        # restaurants = gj["features"]
        # #prepare payload for restaurants
        # query = ('[bbox:53.335895921229486,-6.279885614975843,53.364382211264974,-6.21551259861842]'
        #          '[out:json] [timeout:25];'
        #          'nwr["amenity"="restaurant"](53.335895921229486,-6.279885614975843,53.364382211264974,-6.21551259861842);'
        #          'out geom;')
        # payload = "data=" + quote(query)
        #
        # #send post fetch request to api
        # response = requests.post("https://overpass-api.de/api/interpreter", data=payload)

        #get json response
        # restaurant_json = response.json()
        # restaurants = restaurant_json.get("elements")
        #process each restaurant
        restaurants = gpd.read_file("FoodieHub/data/amenities.geojson")
        restaurants.dropna(subset=['name'], inplace=True)
        restaurants.drop_duplicates(subset=['name'])
        restaurants.fillna("",inplace=True)
        for index, restaurant in restaurants.iterrows():
            address = (str(restaurant.get("addr:housenumber", "")) + " " + str(restaurant.get("addr:street", "")) + " " +
            str(restaurant.get("addr:city", "")) + " " + str(restaurant.get("addr:postcode", "")))

            address = "" if address.isspace() else address
            type, id = restaurant.get("id").split("/")
            building=None
            if type == "node":
                point = GEOSGeometry(str(restaurant.get("geometry")))
            else:
                building = GEOSGeometry(str(restaurant.get("geometry")))
                point = Point(
                    building.centroid.x,
                    building.centroid.y,
                    srid=4326
                )
            amenity = Amenity(
                id=id,
                type=restaurant.get("amenity"),
                name=restaurant.get("name"),
                address=address,
                cuisine=restaurant.get("cuisine", ""),
                location=point,
                building=building
            )
            amenity.save()
        print("Amenities loaded successfully")
