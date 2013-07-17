# HandleBar #
HandleBar is my prototype project for the OS X version. The current master is pretty stable but development is stopped for now.
Comments, ideas or suggestions are welcome any time.

## About ##
HandleBar monitors directories for new video files. These video files are converted in a iTunes supported format using the HandbrakeCLI, tagged with the right metadata and artwork and copied to iTunes. If any can be found, subtitles are also added in the prefered language. All can be monitored using the webinterface.

Check [HandleBarApp](https://github.com/yo-han/HandleBarApp) for a the OS X version of this code.

## Requirements ##
If you plan to use the handleBar subtitles service `lxml` is required. Installing `lxml` is easy:

`$ sudo easy_install lxml`

## Run ##
Change config.plist to your needs.

`$ convert.py start #starts the convert daemon`

`$ web.py start #starts the webinterface`

`$ reSub.py #searches for subtitles for files without and converted with HandleBar`

## HandleBar wouldn't be possible without: ##
Unix Daemon by Sander Marechal [website](http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/)  
Tornado [website](http://www.tornadoweb.org/)  
Subliminal [website](http://subliminal.readthedocs.org/en/latest/)  
Guessit [website](https://github.com/wackou/guessit)  
Pync [website](https://github.com/setem/pync)  
tvdb_api [website](https://github.com/dbr/tvdb_api)  
themoviedb [website](https://github.com/dbr/themoviedb)  
SublerCLI [website](http://code.google.com/p/subler/)  
HandBrakeCLI [website](http://handbrake.fr/)  
send2trash [website](http://hg.hardcoded.net/send2trash/overview)  
python-tvrage [website](https://github.com/ckreutzer/python-tvrage)  


