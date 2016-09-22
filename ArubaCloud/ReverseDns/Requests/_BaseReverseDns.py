from ArubaCloud.base import Request


class BaseReverseDns(Request):
    def __init__(self, *args, **kwargs):
        super(BaseReverseDns, self).__init__(*args, **kwargs)
        # noinspection PyPep8Naming

    def commit(self):
        pass
