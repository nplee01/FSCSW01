class ReturnRecord():
    """
    Record to be returned during rpc calls and
    rpc functions should use this to return the status of the call.

    Caller must instantiate record 
        ret = ReturnRecord()
        ... do something

        ... when error
        ret.set_error('Error...')
        ... or when ok
        set.set_data(data)

        return JsonResponse(ret.to_dict())

    """
    def __init__(self, status=None, error=None, data=None):
        self.status = status or 'OK'    # OK or ERROR
        self.error = error      # Error Message when ERROR
        self.data = data        # Returned Data when OK

    def set_error(self, error):
        # Set error status with message
        self.status = 'ERROR'
        self.error = error

    def set_data(self, data):
        # Status already init with OK
        self.data = data

    def to_dict(self):
        # Need to be a dict to be returned as json
        return {'status': self.status, 'error': self.error, 'data': self.data}
