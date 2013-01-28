#!/usr/bin/env python

from lib import *
from app import *

import time
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

from tornado.options import define, options

define("port", default=8082, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/clear", ClearDBHandler),
            (r"/log", LoggingHandler),
            (r"/failed", FailedHandler),
            (r"/retry", RetryFailedHandler),
            (r"/progress", ProgressHandler),
            (r"/progresssocket", ProgressSocketHandler),
        ]
        settings = dict(
            page_title=u"HandleBar",
            template_path=os.path.join(os.path.dirname(__file__), "media/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "media/static"),
            ui_modules={"File": FileModule},
            xsrf_cookies=True,
            autoescape=None,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = False


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class HomeHandler(BaseHandler):
    def get(self):
        entries = filesTable.list()
        
        self.render("index.tpl", entries=entries, tabActive='home')

class LoggingHandler(BaseHandler):
	def get(self):
	    
	    data_file = open('/tmp/handleBarError.log', 'r')
	    log = data_file.readlines()[-2000:]
	    filteredLog = []
	
	    for line in log:
	    
	        if self.get_argument('filter', 'on') is 'on':
	        	if line.find('DEBUG') > 0:
	        		continue

	        filteredLog.append(line)
	       
	    filteredLog.reverse()
	    
	    self.render("log.tpl", log=filteredLog, tabActive='log')

class FailedHandler(BaseHandler):
    def get(self):
    
    	list = os.listdir(projectDir + '/' + DebugFailedPath) 
    	
        self.render("failed.tpl", entries=list, tabActive='failed')
        
class RetryFailedHandler(BaseHandler):
    def get(self):
    
    	parseFailedFiles()
    
    	self.redirect('/failed')
    	
class ClearDBHandler(BaseHandler):
    def get(self):
    
    	filesTable.clearDb()
    
    	self.redirect('/failed')
    	
class ProgressHandler(BaseHandler):
    def get(self):
    
		hb = os.system('ps ax | grep -v grep | grep HandBrakeCLI > /dev/null')
		
		if hb == 0:
			with open("/tmp/handleBarEncode.status") as f:
				line = unicode(f.readline(),'utf8')
			
			log = line.rsplit('\r')[-1]
		
			self.write(log)
		else:
			self.write('none')

class ProgressSocketHandler(tornado.websocket.WebSocketHandler):
    
    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
          print "WebSocket opened"
		        
    def on_message(self, message):
        
		hb = os.system('ps ax | grep -v grep | grep HandBrakeCLI > /dev/null')
		
		if hb == 0:
			with open("/tmp/handleBarEncode.status") as f:
				line = unicode(f.readline(),'utf8')
			
			log = line.rsplit('\r')[-1]
		
			self.write_message(log)
		else:
			self.write_message('nothing enconding')        			
			
			
class FileModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/file.tpl", entry=entry)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

    
class WebDaemon(Daemon):
	def run(self):
		while True:			
			main()
        	 
if __name__ == "__main__":

	daemon = WebDaemon('/tmp/web-daemon.pid', '/dev/null', '/tmp/handleBarOut.log', '/tmp/handleBarError.log')
	
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
