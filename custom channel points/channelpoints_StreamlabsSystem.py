#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random
import time
import codecs
import threading
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


ScriptName = "custom channel points"
Website = "https://www.slalty.com"
Description = "Contains logic for custom channel point scripts"
Creator = "DanielF737"
Version = "1.4.2"

ReadMeFile = os.path.join(os.path.dirname(__file__), "readme.txt")
settings = {}

threads = []

def OpenReadMe():
  os.startfile(ReadMeFile)
  return

def CallbackLogger(response):
  """ Logs callback error response in scripts logger. """
  parsedresponse = json.loads(response)
  if parsedresponse["status"] == "error":
    Parent.Log("OBS Remote", parsedresponse["error"])
  return

def Bonk():
  # Parent.Log("Bonk", "Starting")
  Parent.SetOBSSourceRender(settings["bonk-sound"], True, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-image"], True, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-cam"], True, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-sound"], True, settings["bonk-wide-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-image"], True, settings["bonk-wide-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-cam"], True, settings["bonk-wide-scene"], CallbackLogger)
  time.sleep(2)
  Parent.SetOBSSourceRender(settings["bonk-sound"], False, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-image"], False, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-cam"], False, settings["bonk-square-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-sound"], False, settings["bonk-wide-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-image"], False, settings["bonk-wide-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["bonk-cam"], False, settings["bonk-wide-scene"], CallbackLogger)
  # Parent.Log("Bonk", "Complete")
  return
  
def Upsidedown():
  # Parent.Log("Upsidedown", "Starting")
  Parent.SetOBSSourceRender(settings["upside-scene"], True, settings["upside-cam"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["upside-sound"], True, settings["upside-cam"], CallbackLogger)
  time.sleep(15)
  Parent.SetOBSSourceRender(settings["upside-scene"], False, settings["upside-cam"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["upside-sound"], False, settings["upside-cam"], CallbackLogger)
  # Parent.Log("Upsidedown", "Complete")
  return

def Cunt():
  # Parent.Log("Cunt", "Starting")
  Parent.SetOBSSourceRender(settings["cunt-graphic"], True, settings["cunt-cam"], CallbackLogger)
  time.sleep(7)
  Parent.SetOBSSourceRender(settings["cunt-graphic"], False, settings["cunt-cam"], CallbackLogger)
  # Parent.Log("Cunt", "Complete")
  return
  

def Init():
  global settings
  work_dir = os.path.dirname(__file__)
  
  try:
    with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
      settings = json.load(json_file, encoding='utf-8-sig')
    
  except Exception, e:
    Parent.Log("UI", str(e))
    settings = {
      "bonk-id": "",
      "bonk-square-scene": "",
      "bonk-wide-scene": "",
      "bonk-sound": "",
      "bonk-image": "",
      "bonk-cam": "",
      "upside-id": "",
      "upside-scene": "",
      "upside-cam": "",
      "upside-sound": "",
      "cunt-id": "",
      "cunt-graphic": "",
      "cunt-cam": ""
    }
  return

def Execute(data):
  username=data.UserName
  time = str(datetime.now())

  if settings["bonk-id"] in data.RawData:
    Parent.SendStreamMessage('Bonking Dan...')
    t = threading.Thread(target=Bonk)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Bonk at " + time)
    return
  if settings["upside-id"] in data.RawData:
    Parent.SendStreamMessage('Dan be careful you\'re upside down!')
    t = threading.Thread(target=Upsidedown)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Upsidedown at " + time)
    return
  if settings["cunt-id"] in data.RawData:
    Parent.SendStreamMessage('Come on boys, don\'t be such a cunt!')
    t = threading.Thread(target=Cunt)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Cunt at " + time)
    return
  
  return

def Tick():
  return
