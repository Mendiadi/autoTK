
class Options:

    def __init__(self ,supported,**kwargs):
        self._supported_args = supported
        if not self._args_supported(kwargs):
            raise Exception("args not supported")
        self._options =  kwargs




    @property
    def supported(self):
        return self._supported_args

    @property
    def options(self):
        return self._options



    def _args_supported(self ,kwargs):
        temp = dict(kwargs)
        for key ,v in temp.items():
            if key not in self._supported_args:
                return False
            if not v :
                kwargs.pop(key)
        return True
