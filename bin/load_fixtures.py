#!/usr/bin/env python

# Script to load our fixtures

# from python
import sys, os, subprocess

import runtest.run_django # Required to run this script
# from django
from django.conf import settings

# our module
from runtest.fixtures.set_audit_user import set_audit_user

def load_app_data(app_name):

    # Goto app home, fix_dir is relative to this.
    curr_dir = os.getcwd()
    os.chdir(settings.BASE_DIR)
    fix_dir = os.path.join(app_name, 'fixtures')
    if os.path.exists(fix_dir):
        try:
            in_file = open(os.path.join(fix_dir, 'load_order.txt'), 'r')
        except IOError:
            # Ignore this app when load order file not defined
            print("No load_order.txt file in " + fix_dir + "... skipping to next app")
            return

        for line in in_file:
            # ignore comment line
            if line.startswith('#') or not line.rstrip():
                continue
            else:
                fix_file = line.strip()
                (name, ext) = os.path.splitext(fix_file)

                if ext == ".py":
                    # Python scripts should set_audit_user for audit logging
                    print("Running python script", fix_dir, fix_file)
                    po = subprocess.Popen("python " + fix_dir + os.sep + fix_file, shell=True)
                    ret = po.wait()
                else:
                    # Audit user shall be nobody because new shell will run loaddata below
                    # and we can't change it to do our set audit user
                    print("Installing fixtures", fix_dir, fix_file)
                    po = subprocess.Popen("django-admin.py loaddata " + fix_dir + os.sep + fix_file, shell=True)
                    ret = po.wait()

        in_file.close()
    # Return to current dir
    os.chdir(curr_dir)

def load_data():

    # For each local App, load its fixtures in app/fixtures
    for app_name in settings.INSTALLED_APPS:
        load_app_data(app_name)

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1]:
        # app_name can be optionally passed in
        load_app_data(sys.argv[1])
    else:
        # load for all apps
        load_data()
