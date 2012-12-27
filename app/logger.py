import logging

class Logger(object):
	
	 def __init__(self, app):
		 
		 self.lg = logging.getLogger(app)
		 
		 logging.basicConfig(filename='/tmp/' + app + '.log',
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
                 
         