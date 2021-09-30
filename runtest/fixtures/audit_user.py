# Create audit user to own fixtures
import os, secrets
import runtest.run_django
from django.contrib.auth.models import User, Permission

FIX_USER = 'fixtures'

def audit_user():
    # Get password from .env (else default to new password which will be unknown)
    pwd = os.environ.get('FIX_USER_PASSWORD', secrets.token_urlsafe()[:10])
    try :
        au = User.objects.get(username=FIX_USER)
        # Allow change password only
        au.set_password(pwd)
    except User.DoesNotExist:
        # Create new user
        au = User.objects.create_user(username=FIX_USER, email=FIX_USER + '@atsc.org.my', password=pwd)
        au.is_staff = True
    # grant perms for admin of our app
    perms = Permission.objects.filter(content_type__app_label__in=['runtest', 'account', 'socialaccount'])
    for pm in perms:
        au.user_permissions.add(pm)
    # Save all
    au.save()

if __name__ == '__main__':
    audit_user()
