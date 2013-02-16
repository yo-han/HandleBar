""" HandleBar """

from app import *
from lib import *

import time

def main():
    reSub()

    
class SubtitleDaemon(Daemon):
	def run(self):
		while True:
						
			main()
			
			time.sleep(3600)
        	 
if __name__ == "__main__":

	daemon = SubtitleDaemon('/tmp/reSub-daemon.pid', '/dev/null', '/tmp/handleBarOut.log', '/tmp/handleBarError.log')
	
	if len(sys.argv) >= 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'test' == sys.argv[1]:
			main()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|test" % sys.argv[0]
        sys.exit(2)

