import telebot
import datetime
import requests


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hello, <b> {message.from_user.first_name} <u>{message.from_user.last_name}.</u> I can tell you about weather' \
           f'Just write weather or simply w to start using me:)</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def website(message):
    bot.send_message(message.chat.id, 'print "w"')

@bot.message_handler(content_types=['text'])
def get_user_txt(message):
    if message.text.lower() in ['hi', 'hello', 'good morning', 'greetings']:
        bot.send_message(message.chat.id, "Hi there")
    elif message.text.lower() in ['weather', 'tell me about the weather', 'w']:
        bot.send_message(message.chat.id, "What city?")
        bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(message.chat.id, f'I do not get you', parse_mode='html')

def get_weather(message):
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric")
        data = r.json()
        # pprint(data)

        town = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        weather = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        bot.send_message(message.chat.id, f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***')
        bot.send_message(message.chat.id, f' Weather in {town}({country}) \n The temperature: {temp}C \n The humidity: {humidity}% \n Pressure is {pressure} \n Overall: {weather} \n Wind speed: {wind_speed} \n Sunrise: {sunrise} \n Sunset: {sunset}')
    except Exception as ex:
        bot.send_message(message.chat.id, 'could not find the city')

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Nice photo, man')



bot.polling(none_stop=True)
