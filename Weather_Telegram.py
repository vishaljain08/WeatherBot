from geotext import GeoText
import json
import requests
from nltk import word_tokenize

TOKEN = "990580047:AAH4BUQiXrRB9vPNETGKsLC7qcu_L4P8-tc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


    

api_key = "&appid=e645310ebde45d4a41ae3d852cc14d96"
unit="&units=metric"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

print ("Welcome to WeatherBot") 
print ("What would you like me to?")
user_input, chat = get_last_chat_id_and_text(get_updates())
city = GeoText(user_input).cities
city_string = city[0]
api_call = base_url + city_string + api_key + unit
request = requests.get(api_call).json()
print (api_call)
temp = str(int(request['main']['temp']))
temp_max = str(int(request['main']['temp_max']))
temp_min = str(int(request['main']['temp_min']))
feels_like = str(int(request['main']['feels_like']))
pressure = str(int(request['main']['pressure']))
humidity = str(int(request['main']['humidity']))
wind_speed = str(int(request['wind']['speed']))
weather_main = request['weather'][0]['main']
weather_description = request['weather'][0]['description']
city_name = request ['name']
country = request['sys'] ['country']
place_name = city_name + ", " + country
words = word_tokenize(user_input)
a=0
for i in words:
    if i.lower() == "weather":
        a=1
    elif i.lower() in ["temp" , "temperature"]:
        a=2
    elif i.lower() in ["wind", "air]"]:
        a=3

#Funtions

def PrintWeather():
    text = place_name + "\n" + "Weather: "+weather_main +"\n"+ "Weather Description: "+weather_description
    send_message(text, chat)

def PrintTemp():
    text = place_name + "\n" + "Current Temperature: "+temp+"°C" + "\n" + "Feels Like: "+feels_like+"°C" + "\n" + "Maximum Temperature: "+temp_max+"°C" + "\n" + "Minimum Temperature: "+temp_min+"°C"
    send_message(text, chat)

def PrintWind():
    text = place_name + "\n" + "Wind Speed: "+wind_speed + " kmph" + "\n" + "Humidity: " + humidity + "%"
    send_message(text, chat)

#Printings
print (place_name)

if a==1:
    PrintWeather()
    
if a==2:
    PrintTemp()
    
if a==3:
    PrintWind()

