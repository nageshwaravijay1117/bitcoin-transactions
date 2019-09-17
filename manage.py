#!/usr/bin/env python
import os, sys
from flask_script import Manager, Shell, Server
from app import app

manager = Manager(app)

# run the app
manager.add_command(
    "startserver",
    Server(port=5002, host='0.0.0.0', threaded=True))


if __name__ == '__main__':
	if sys.version_info.major < 3:
		current_version = '.'.join(str(x) for x in sys.version_info[:3])
		raise ImportError('Python version 3 or Higher required. Current version: %s' % current_version)
	manager.run()

