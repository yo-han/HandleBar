import ConfigParser, os

path = os.path.abspath(os.path.dirname(__file__)) + "/../"

""" Config """
Config = ConfigParser.ConfigParser()
Config.read(path + "config.ini")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
    
DebugMode  = Config.getboolean("HandleBarConfig", "Debug")
NotificationOn  = Config.getboolean("HandleBarConfig", "NotificationOn")
HandbrakeCLIPath = path + Config.get("HandleBarConfig","HandbrakeCLIPath")
DebugRemovePath = path + Config.get("HandleBarConfig","DebugRemovePath")
MediaPathsString = Config.get("HandleBarConfig","MediaPaths")

FileTypeString = Config.get("HandleBarConfig","FileTypes")
HandBrakePreset = Config.get("HandleBarConfig","HandBrakePreset")
HandBrakeLanguage = Config.get("HandleBarConfig","HandBrakeLanguage")

MediaPaths = MediaPathsString.split(',')
FileTypes = FileTypeString.split(',')
