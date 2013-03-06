import ConfigParser, os, sys, shutil, plistlib

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
		
def fileExists(file):
	filePath = path + 'app/default/' + file
	if not os.path.exists(configPath + '/' + file):
		shutil.copyfile(filePath, configPath + '/' + file)	
		
fileExists('config.plist')
fileExists('handleBar.db')
 
""" Config """
Config = plistlib.readPlist(configPath + '/config.plist')
    
DebugMode  = Config["Debug"]
NotificationOn  = Config[ "NotificationOn"]

HandbrakeCLIPath = path + Config["HandbrakeCLIPath"]
DebugRemovePath = Config["DebugRemovePath"]
DebugFailedPath = Config["DebugFailedPath"]
SubtitlePath = Config["SubtitlePath"]
ReadyPath = Config["ReadyPath"]
MediaPaths = Config["MediaPaths"]
ReSubSearchPaths = Config["ReSubSearchPaths"]
HandleBarConfigPath = configPath
HandleBarBinPath = path

FileTypes = Config["FileTypes"]
HandBrakePreset = Config["HandBrakePreset"]
HandBrakeLanguage = Config["HandBrakeLanguage"]
SubtitleLanguage = Config["SubtitleLanguage"]
SubtitleLanguageISO = Config["SubtitleLanguageISO"]

dirExists(path + DebugRemovePath)
dirExists(path + DebugFailedPath)
dirExists(path + SubtitlePath)
dirExists(path + ReadyPath)
dirExists(path + 'media/images')