from ._BaseReverseDns import BaseReverseDns


class SetEnqueueSetReverseDns(BaseReverseDns):
    def __init__(self, *args, **kwargs):
        """
        Assign one or more PTR record to a single IP Address
        :type IP: str
        :type Host: list[str]
        :param IP: (str) The IP address to configure
        :param Host: (list[str]) The list of strings representing PTR records
        """
        try:
            self.IP = kwargs.pop('IP')
        except KeyError:
            raise Exception('IP parameter cannot be null.')
        try:
            self.Hosts = kwargs.pop('Hosts')
        except KeyError:
            raise Exception('Hosts parameter cannot be null.')
        super(SetEnqueueSetReverseDns, self).__init__(*args, **kwargs)

    def commit(self):
        return self._commit()
