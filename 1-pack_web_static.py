#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static folder
Using do_pack
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates .tgz
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filePath = 'versions/web_static_{}.tgz'.format(now)

    local('mkdir -p versions/')
    createArchive = local('tar -cvzf {} web_static/'.format(filePath))

    if createArchive.succeeded:
        return filePath
