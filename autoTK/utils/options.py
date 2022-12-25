import copy


class Options:

    def __init__(self, supported, **kwargs):
        self._supported_args = supported

        if not self._args_supported(kwargs):
            raise Exception("args not supported")
        self._options = kwargs
        self._font = ["none",10,"normal"]

    def update_font(self):


        f_style=self._options.pop("font style", self._font[2])
        self._font[2] = f_style
        f_size =self._options.pop("font size", self._font[1])
        self._font[1] = f_size
        font =  self._options.pop("font type", self._font[0])

        self._font[0] = font
        self._options["font"] =tuple(self._font)
        print(self.options['font'])

    def copy(self):
        x = Options(self._supported_args,**self.options)
        x._font = self._font
        return x

    @property
    def supported(self):
        return self._supported_args

    @property
    def options(self):
        return self._options

    def _args_supported(self, kwargs):
        temp = dict(kwargs)

        for key, v in temp.items():

            if key not in self._supported_args:
                return False
            if not v:
                kwargs.pop(key,0)

        return True
