import urllib.request
import base64
import time
from mijia.mijia_poller import MijiaPoller, \
    MI_HUMIDITY, MI_TEMPERATURE, MI_BATTERY

# Settings for the blynk server

# url: http://blynkserver/auth_token/update/pin?value=value

blynkserver = "192.168.31.222"
auth_token = ""
temp_pin = "V0"
humidity_pin = "V1"
battery_pin = "V2"

def blynkrequest(url):
  print(url)
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
  return response.read()

def postblynkrequest(url, payload):
  data = parse.urlencode(payload).encode()
  req =  request.Request(url, data=data) # this will make the method "POST"
  resp = request.urlopen(req)

def update(address):

    poller = MijiaPoller(address)


    loop = 0
    try:
        temp = poller.parameter_value(MI_TEMPERATURE)
    except:
        temp = "Not set"

    while loop < 2 and temp == "Not set":
        print("Error reading value retry after 5 seconds...\n")
        time.sleep(5)
        poller = MijiaPoller(address)
        loop += 1
        try:
            temp = poller.parameter_value(MI_TEMPERATURE)
        except:
            temp = "Not set"

    if temp == "Not set":
        print("Error reading value\n")
        return

    global blynkserver
    global auth_token
    global temp_pin
    global humidity_pin
    global battery_pin

    print("Mi Sensor: " + address)
    print("Firmware: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}°C".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Humidity: {}%".format(poller.parameter_value(MI_HUMIDITY)))
    print("Battery: {}%".format(poller.parameter_value(MI_BATTERY)))

    val_bat  = "{}".format(poller.parameter_value(MI_BATTERY))

    val_temp = "{}".format(poller.parameter_value(MI_TEMPERATURE))
    val_hum = "{}".format(poller.parameter_value(MI_HUMIDITY))

    # val_comfort = "0"
    # if float(val_hum) < 40:
    #     val_comfort = "2"
    # elif float(val_hum) <= 70:
    #     val_comfort = "1"
    # elif float(val_hum) > 70:
    #     val_comfort = "3"

    # http://blynkserver/auth_token/update/pin?value=value

    # push temp
    blynkrequest("http://" + blynkserver + "/" + auth_token + "/update/" + temp_pin + "?value=" + val_temp)

    if val_temp < 20:
      # send notification
      # http://blynk-cloud.com/auth_token/notify
      postblynkrequest("http://" + blynkserver + "/" + auth_token + "/notify", {'body': 'Температура у ежа меньше 20 градусов!'})


    # push humidity
    blynkrequest("http://" + blynkserver + "/" + auth_token + "/update/" + humidity_pin + "?value=" + val_hum)


print("\n1: updating")
update("4C:65:A8:D5:5C:AC")




