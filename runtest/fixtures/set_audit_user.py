# Set admin user to be captured in audit trail
from django.contrib.auth.models import User
from runtest.threadlocals import set_user

def set_audit_user():
    try:
        # superuser should be the first user created during syncdb
        user = User.objects.get(pk=1)
        set_user(user)
    except User.DoesNotExist:
        pass
