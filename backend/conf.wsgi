#!/usr/bin/python
import sys, os, logging 
logging.basicConfig(stream=sys.stderr)
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dir,"venv/lib/python3.12/site-packages"))
sys.path.insert(0, dir)
from app import app as application
application.secret_key = 'secret key'
