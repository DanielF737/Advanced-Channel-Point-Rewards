import os
import sys
import clr
import json
import random
import time
import codecs
import System
import threading
from datetime import datetime

# Include the assembly with the name AnkhBotR2
clr.AddReference([asbly for asbly in System.AppDomain.CurrentDomain.GetAssemblies() if "AnkhBotR2" in str(asbly)][0])
import AnkhBotR2

# Twitch PubSub library and dependencies
lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Lib")
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "Microsoft.Extensions.Logging.Abstractions.dll"))
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "TwitchLib.Communication.dll"))
clr.AddReferenceToFileAndPath(os.path.join(lib_path, "TwitchLib.PubSub.dll"))
from TwitchLib.PubSub import *
from TwitchLib.PubSub.Events import *

# Instead of Parent.GetRequest which was giving me issues
clr.AddReference("System.Net.Http")
from System.Net.Http import HttpClient

ScriptName = "custom channel points"
Website = "https://www.slalty.com"
Description = "Contains logic for custom channel point scripts"
Creator = "DanielF737"
Version = "1.8.9"

# Define Global Variables
path = os.path.dirname(os.path.realpath(__file__))
client = TwitchPubSub()
ReadMeFile = os.path.join(os.path.dirname(__file__), "readme.txt")
settings = {}
threads = []

def OpenReadMe():
  os.startfile(ReadMeFile)
  return

def CallbackLogger(response):
  # Logs callback error response in scripts logger.
  parsedresponse = json.loads(response)
  if parsedresponse["status"] == "error":
    Parent.Log("OBS Remote", parsedresponse["error"])
  return

def Bonk():
  # Parent.Log("Bonk", "Starting")
  Parent.SetOBSSourceRender(settings["bonk-source"], True, settings["bonk-scene"], CallbackLogger)
  time.sleep(3)
  Parent.SetOBSSourceRender(settings["bonk-source"], False, settings["bonk-scene"], CallbackLogger)
  # Parent.Log("Bonk", "Complete")
  return

def Upsidedown():
  # Parent.Log("Upsidedown", "Starting")
  Parent.SetOBSSourceRender(settings["upside-source"], True, settings["upside-scene"], CallbackLogger)
  time.sleep(15)
  Parent.SetOBSSourceRender(settings["upside-source"], False, settings["upside-scene"], CallbackLogger)
  # Parent.Log("Upsidedown", "Complete")
  return

def Cunt():
  # Parent.Log("Cunt", "Starting")
  Parent.SetOBSSourceRender(settings["cunt-graphic"], True, settings["cunt-cam"], CallbackLogger)
  time.sleep(7)
  Parent.SetOBSSourceRender(settings["cunt-graphic"], False, settings["cunt-cam"], CallbackLogger)
  # Parent.Log("Cunt", "Complete")
  return

def SnyderCut():
  # Parent.Log("Snyder", "Starting")
  Parent.SetOBSCurrentScene(settings["snyder-text"], CallbackLogger)
  time.sleep(4.9)
  Parent.SetOBSCurrentScene(settings["snyder-no-text"], CallbackLogger)
  time.sleep(25)
  Parent.SetOBSCurrentScene(settings["snyder-raw-gameplay"], CallbackLogger)
  # Parent.Log("Snyder", "Complete")
  return

def Applegate():
  # Parent.Log("Applegate", "Starting")
  Parent.SetOBSSourceRender(settings["applegate-folder"], True, settings["applegate-game"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["applegate-folder"], True, settings["applegate-chatting"], CallbackLogger)
  time.sleep(13)
  Parent.SetOBSSourceRender(settings["applegate-folder"], False, settings["applegate-game"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["applegate-folder"], False, settings["applegate-chatting"], CallbackLogger)
  # Parent.Log("Applegate", "Complete")
  
def Punch():
  # Parent.Log("Punch", "Starting")
  suf = time.gmtime()[5] % 10
  source = "%s%s"%(settings["punch-prefix"], suf)
  # Parent.Log("Punch", source)
  Parent.SetOBSSourceRender(source, True, settings["punch-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["punch-sound"], True, settings["punch-scene"], CallbackLogger)
  time.sleep(1.5)
  Parent.SetOBSSourceRender(source, False, settings["punch-scene"], CallbackLogger)
  Parent.SetOBSSourceRender(settings["punch-sound"], False, settings["punch-scene"], CallbackLogger)
  # Parent.Log("Punch", "Complete")


# Initialize Data (Only called on load)
def Init():
  oauth = GetOAuth()
  auth = 'OAuth ' + oauth.replace("oauth:", "")
  
  # headers = {'Authorization': auth}
  # t = Parent.GetRequest("https://id.twitch.tv/oauth2/validate", headers)
  
  httpclient = HttpClient()
  httpclient.DefaultRequestHeaders.Add("Authorization", auth)
  t = httpclient.GetStringAsync("https://id.twitch.tv/oauth2/validate")
  data = ""
  try:
    t.Wait()
    data = t.Result

  except:
    Parent.Log("Custom-Main", 'Error with OAuth')
    return
  casterid = json.loads(data)['user_id']

  # Register the client to listen to reward redeems
  client.OnPubSubServiceConnected += OnPubSubConnected
  client.OnRewardRedeemed += OnRewardRedeemed
  client.ListenToRewards(casterid)
  client.Connect()

  global settings
  work_dir = os.path.dirname(__file__)
  
  try:
    with codecs.open(os.path.join(work_dir, "settings.json"), encoding='utf-8-sig') as json_file:
      settings = json.load(json_file, encoding='utf-8-sig')
    
  except Exception, e:
    Parent.Log("UI", str(e))
    settings = {
      "bonk-name": "",
      "bonk-source": "",
      "bonk-scene": "",
      "upside-name": "",
      "upside-source": "",
      "upside-scene": "",
      "cunt-name": "",
      "cunt-graphic": "",
      "cunt-cam": "",
      "snyder-name": "",
      "snyder-text": "",
      "snyder-no-text": "",
      "snyder-raw-gameplay": "",
      "applegate-name": "",
      "applegate-game": "",
      "applegate-chatting": "",
      "applegate-folder": "",
      "punch-name": "",
      "punch-prefix": "",
      "punch-sound": "",
      "punch-scene": ""
    }

def Execute(data):
  pass

def Tick():
  pass

# Cleanup script when script is unloaded/reloaded
def Unload():
  global client
  client.OnPubSubServiceConnected -= OnPubSubConnected
  client.OnRewardRedeemed -= OnRewardRedeemed
  client.Disconnect()
  del client

def GetOAuth():
  vmloc = AnkhBotR2.Managers.GlobalManager.Instance.VMLocator
  return vmloc.StreamerLogin.Token

def OnPubSubConnected(s, e):
  client.SendTopics()
  
# When a channelpoint rewards is redeemed
def OnRewardRedeemed(s, e):
  username=e.DisplayName
  time = str(datetime.now())

  if e.RewardTitle == settings["bonk-name"]:
    Parent.SendStreamMessage('Bonking Dan...')
    t = threading.Thread(target=Bonk)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Bonk at " + time)
    return
  if e.RewardTitle == settings["upside-name"]:
    Parent.SendStreamMessage('Dan be careful you\'re upside down!')
    t = threading.Thread(target=Upsidedown)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Upsidedown at " + time)
    return
  if e.RewardTitle == settings["cunt-name"]:
    Parent.SendStreamMessage('Come on boys, don\'t be such a cunt!')
    t = threading.Thread(target=Cunt)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Cunt at " + time)
    return
  if e.RewardTitle == settings["snyder-name"]:
    Parent.SendStreamMessage('Reducing aspect ratio to appease Zac\'s vision...')
    t = threading.Thread(target=SnyderCut)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Snyder Cut at " + time)
    return
  if e.RewardTitle == settings["applegate-name"]:
    Parent.SendStreamMessage('Lets give a quick shout-out to Christina Applegate')
    t = threading.Thread(target=Applegate)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Applegate at " + time)
    return
  if e.RewardTitle == settings["punch-name"]:
    Parent.SendStreamMessage('Beating the shit out of Dan...')
    t = threading.Thread(target=Punch)
    threads.append(t)
    t.start()
    Parent.Log("Custom-Main", username + " Executed Punch at " + time)
    return