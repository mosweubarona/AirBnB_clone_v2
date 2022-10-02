#!/usr/bin/python3
"""pack and deploy content to server
"""
from fabric.api import local, env, run, put
from datetime import datetime
import os
env.hosts = ['35.168.111.24', '3.236.88.192']
env.user = 'ubuntu'


def do_pack():
    """Generates .tgz
    """
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filePath = 'versions/web_static_{}.tgz'.format(now)

    local('mkdir -p versions/')
    createArchive = local('tar -cvzf {} web_static/'.format(filePath))

    if createArchive.succeeded:
        return filePath


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    """
    if os.path.isfile(archive_path) is False:
        return False
    fullFile = archive_path.split("/")[-1]
    folder = fullFile.split(".")[0]

    if put(archive_path, "/tmp/{}".format(fullFile)).failed is True:
        print("Uploading archive to /tmp/ failed")
        return False

    if run("rm -rf /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Deleting folder with archive(if already exists) failed")
        return False

    if run("mkdir -p /data/web_static/releases/{}/".
           format(folder)).failed is True:
        print("Creating new archive folder failed")
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fullFile, folder)).failed is True:
        print("Uncompressing archive to failed")
        return False

    if run("rm /tmp/{}".format(fullFile)).failed is True:
        print("Deleting archive from /tmp/ directory dailed")
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".
           format(folder, folder)).failed is True:
        print("Moving content to archive folder before deletion failed")
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(folder)).failed is True:
        print("Deleting web_static folder failed")
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        print("Deleting 'current' folder failed")
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(folder)).failed is True:
        print("Creating new symbolic link to new code version failed")
        return False

    print("New version deployed!")
    return True


def deploy():
    """pack web_static content and deploy it to web servers
    """
    pack = do_pack()
    if pack:
        return do_deploy(pack)
    return False
