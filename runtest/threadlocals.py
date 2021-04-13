# This middleware will save the logged in user (request.user) in thread local memory so that
# all our programs that has no access to the request object can retrieve the logged in user.
# This is used for audit purposes. Program need to check for request.user.is_authenticated 
# for anonymous users.
#
import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

# Non-django processes should call this to set user.
# You can then use get_current_user()
def set_user(user):
    # A User instance must be passed in
    _thread_locals.user = user

class ThreadLocals(object):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    Seems that threadlocals is not cleared of previous user's
    values, so we need to change it on every changed of logged in User.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store authenticated User Object, if different from previous
        if getattr(request, 'user', None) != getattr(_thread_locals, 'user', None):
            _thread_locals.user = getattr(request, 'user', None)

        response = self.get_response(request)

        return response
