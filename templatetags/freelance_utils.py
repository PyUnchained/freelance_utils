import os
from django import template
from django.conf import settings
from decimal import *

register = template.Library()

@register.filter
def filesize(upload):
    """Returns the filesize of the filename given in upload.file"""

    root_dir = settings.MEDIA_ROOT
    file_path = os.path.join(root_dir, str(upload.file))
    try:
    	size = float(os.path.getsize(file_path))/1024/1024
    	s = "{0:.2f}Mb".format(size)
    except OSError as e:
    	s = file_path
    
    return s