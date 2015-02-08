import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'newproject.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
path = '/home/jchinte/workspace/newproject/src/newproject/'
if path not in sys.path:
	sys.path.append(path)
path = '/home/jchinte/workspace/newproject/src/'
if path not in sys.path:
	sys.path.append(path)

"""
import sys

sys.path.insert(0, '/home/jchinte/workspace/newproject/src/newproject')

import settings

import django.core.management
django.core.management.setup_environ(settings)
utility = django.core.management.ManagementUtility()
command = utility.fetch_command('runserver')

command.validate()

import django.conf
import django.utils

django.utils.translation.activate(django.conf.settings.LANGUAGE_CODE)

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
"""
