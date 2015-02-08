import os, sys
sys,path.append('/home/jchinte/workspace/newproject/src')
sys,path.append('/home/jchinte/workspace/newproject/src/newproject')
os.environ['DJANGO_SETTINGS_MODULE']='newproject.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

