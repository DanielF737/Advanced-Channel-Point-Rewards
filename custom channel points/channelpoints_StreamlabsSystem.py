#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random
import time
import codecs
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


ScriptName = "custom channel points"
Website = "https://www.slalty.com"
Description = "Contains logic for custom channel point scripts"
Creator = "DanielF737"
Version = "1.2.8"

ReadMeFile = os.path.join(os.path.dirname(__file__), "ReadMe.txt")

settings = {}

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
  Parent.Log("Bonk", "Starting")
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
  Parent.Log("Bonk", "Complete")
  return
  
def Upsidedown():
  Parent.Log("Upsidedown", "Starting")
  Parent.SetOBSSourceRender(settings["upside-scene"], True, settings["upside-cam"], CallbackLogger)
  time.sleep(15)
  Parent.SetOBSSourceRender(settings["upside-scene"], False, settings["upside-cam"], CallbackLogger)
  Parent.Log("Upsidedown", "Complete")
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
      "bonk-id": "a37dd922-0075-4fd0-9527-79c2dc9384b8",
      "bonk-square-scene": "bonk-square-scene",
      "bonk-wide-scene": "Fullscreen Cam",
      "bonk-sound": "bonk",
      "bonk-image": "BONK",
      "bonk-cam": "Bonk",
      "upside-id": "eabd6c20-8a5b-4ba2-9063-e1dc9e0c5200",
      "upside-scene": "Webcam Upside Down",
      "upside-cam": "Webcam"
    }
  return

def Execute(data):
  Parent.Log("Test", data.RawData)
  if settings["bonk-id"] in data.RawData:
    Bonk()
    Parent.SendStreamMessage('Bonking Dan...')
    Parent.Log("Custom-Main", "Executed Bonk")
    return
  if settings["upside-id"] in data.RawData:
    Upsidedown()
    Parent.SendStreamMessage('Dan be careful you\'re upside down!')
    Parent.Log("Custom-Main", "Executed Upsidedown")
    return
  
  # Parent.Log("Yeetus", "done")
  return

def Tick():
  return
