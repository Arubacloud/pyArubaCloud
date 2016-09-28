from NotificationType import NotificationType


class NotificationContact(object):
    def __init__(self, contactValue=str(), loadBalancerContactID=int(), contactType=NotificationType.Email):
        self.ContactValue = contactValue
        self.LoadBalancerContactID = loadBalancerContactID
        self.Type = contactType
