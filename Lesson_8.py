import json
import folium
import requests
from geopy import distance


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_user_distance(coffe_shop_new):
    return coffe_shop_new['distance']


if __name__ == '__main__':

    with open('coffee.json', 'r', encoding="CP1251") as my_file:
        file_contents = my_file.read()

    coffe_shops = json.loads(file_contents)

    apikey = '2f78ceff-5026-480d-a361-209bf66f3386'

    point = input('Где вы находитесь?   ')
    coordinates = fetch_coordinates(apikey, point)
    print('Ваши координаты: ', coordinates)

    m = folium.Map(location=(coordinates), zoom_start=14)
    m.save("index.html")

    coffe_shops_new = []

    for coffe_shop in coffe_shops:
        coffe_shop_new = dict()
        coffe_shop_new['title'] = coffe_shop['Name']
        coffe_shop_coordinates_1 = coffe_shop['geoData']['coordinates'][1]
        coffe_shop_coordinates_2 = coffe_shop['geoData']['coordinates'][0]
        coffe_shop_coordinates = [
                                  coffe_shop_coordinates_1,
                                  coffe_shop_coordinates_2
                                 ]
        coffe_shop_new['distance'] = distance.distance(coffe_shop_coordinates, coordinates).km
        coffe_shop_new['latitude'] = coffe_shop_coordinates_1
        coffe_shop_new['longitude'] = coffe_shop_coordinates_2
        coffe_shops_new.append(coffe_shop_new)
    coffe_shops_sorted = sorted(coffe_shops_new, key=get_user_distance)

    nearest_coffe_shops = []
    for i in range(0, 5):
        nearest_coffe_shop = coffe_shops_sorted[i]
        nearest_coffe_shops.append(nearest_coffe_shop)
        folium.Marker(
        location=[nearest_coffe_shop['latitude'], nearest_coffe_shop['longitude']],
        tooltip="Click me!",
        popup="Timberline Lodge",
        icon=folium.Icon(color="green"),
        ).add_to(m)

    m.save("index.html")
