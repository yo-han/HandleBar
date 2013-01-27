import ConfigParser, os, sys

path = os.path.abspath(os.path.dirname(__file__)) + "/../"

sys.path.insert(0, path)
sys.path.insert(0, os.path.join(path, 'lib'))
		
""" App support path """
try:
	pf = file(path + "../configPath",'r')
	appSupportPath = pf.read().strip()
	pf.close()
except IOError:
	print "Not running in menulet"

if path.find("HandleBarApp.app") is not -1:
	configPath = appSupportPath
else:
	configPath = path

""" Config """
Config = ConfigParser.ConfigParser()
Config.read(configPath + "/config.ini")

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

def dirExists(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)
    
DebugMode  = Config.getboolean("HandleBarConfig", "Debug")
NotificationOn  = Config.getboolean("HandleBarConfig", "NotificationOn")

HandbrakeCLIPath = path + Config.get("HandleBarConfig","HandbrakeCLIPath")
DebugRemovePath = Config.get("HandleBarConfig","DebugRemovePath")
DebugFailedPath = Config.get("HandleBarConfig","DebugFailedPath")
SubtitlePath = Config.get("HandleBarConfig","SubtitlePath")
ReadyPath = Config.get("HandleBarConfig","ReadyPath")
MediaPathsString = Config.get("HandleBarConfig","MediaPaths")
HandleBarConfigPath = configPath
HandleBarBinPath = path

FileTypeString = Config.get("HandleBarConfig","FileTypes")
HandBrakePreset = Config.get("HandleBarConfig","HandBrakePreset")
HandBrakeLanguage = Config.get("HandleBarConfig","HandBrakeLanguage")

MediaPaths = MediaPathsString.split(',')
FileTypes = FileTypeString.split(',')

dirExists(path + DebugRemovePath)
dirExists(path + DebugFailedPath)
dirExists(path + SubtitlePath)
dirExists(path + ReadyPath)
	
