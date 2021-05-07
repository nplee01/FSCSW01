import os, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Load our application fixtures'

    def add_arguments(self, parser):
         parser.add_argument(
            '--app', dest='app_label',
            help='Only look for fixtures in the specified app.',
        )

    def handle(self, *args, **options):
        if options['app_label']:
            self.load_app_data(options['app_label'])
        else:
            # Else load all installed apps fixtures
            self.load_data()

    def load_app_data(self, app_name):

        # Goto app home, fix_dir is relative to this.
        curr_dir = os.getcwd()
        os.chdir(settings.BASE_DIR)
        fix_dir = os.path.join(app_name, 'fixtures')
        if os.path.exists(fix_dir):
            try:
                in_file = open(os.path.join(fix_dir, 'load_order.txt'), 'r')
            except IOError:
                # Ignore this app when load order file not defined
                raise CommandError("No load_order.txt file in " + fix_dir + "... skipping to next app")
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
                        po = subprocess.Popen("python " + fix_dir + os.sep + fix_file, shell=True)
                        ret = po.wait()
                    else:
                        # Audit user shall be nobody because new shell will run loaddata below
                        # and we can't change it to do our set audit user
                        # print("Installing fixtures", fix_dir, fix_file)
                        po = subprocess.Popen("django-admin.py loaddata " + fix_dir + os.sep + fix_file, shell=True)
                        ret = po.wait()

            in_file.close()
        # Return to current dir
        os.chdir(curr_dir)

    def load_data(self):

        # For each local App, load its fixtures in app/fixtures
        for app_name in settings.INSTALLED_APPS:
            self.load_app_data(app_name)

