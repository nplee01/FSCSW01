# Set admin user to be captured in audit trail
from django.contrib.auth.models import User
from runtest.threadlocals import set_user
from .audit_user import FIX_USER

def set_audit_user():
    try:
        user = User.objects.get(username=FIX_USER)
        set_user(user)
    except User.DoesNotExist:
        pass
