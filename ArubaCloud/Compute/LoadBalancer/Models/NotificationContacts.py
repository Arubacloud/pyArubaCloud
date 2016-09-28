from NotificationContact import NotificationContact


class NotificationContacts(list):
    def __init__(self, *args, **kwargs):
        super(NotificationContacts, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        assert isinstance(value, NotificationContact), Exception(
            'Expected NotificationContact, got: {}'.format(type(value)))
        super(NotificationContacts, self).__setitem__(key, value)

    def __str__(self):
        super(NotificationContacts, self).__str__()

    def append(self, p_object):
        assert isinstance(p_object, NotificationContact), Exception(
            'Expected NotificationContact, got: {}'.format(type(p_object)))
        super(NotificationContacts, self).append(p_object)

    def insert(self, index, p_object):
        assert isinstance(p_object, NotificationContact), Exception(
            'Expected NotificationContact, got: {}'.format(type(p_object)))
        super(NotificationContacts, self).insert(index, p_object)
