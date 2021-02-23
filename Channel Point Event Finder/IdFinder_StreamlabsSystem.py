ScriptName = "ID Finder"
Website = "https://www.slalty.com"
Description = "Logs message data to find channel point IDs"
Creator = "DanielF737"
Version = "1.0.1"
Command = ""

def Init():
  return

def Execute(data):
  Parent.Log("ID Finder", data.RawData)
  return

def Tick():
  return

