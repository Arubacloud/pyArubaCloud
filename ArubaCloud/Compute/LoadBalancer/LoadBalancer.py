from ArubaCloud.base import ArubaCloudService
from ArubaCloud.Compute.LoadBalancer.Requests import *
import datetime


class LoadBalancer(ArubaCloudService):
    def __init__(self, *args, **kwargs):
        super(LoadBalancer, self).__init__(*args, **kwargs)

    def _call(self, method, *args, **kwargs):
        request = method(Username=self.username, Password=self.password, uri=self.ws_uri, *args, **kwargs)
        response = request.commit()
        return response['Value']

    def create(self, healthCheckNotification, instance, ipAddressResourceId, name, notificationContacts, rules,
               loadBalancerClassOfServiceID=1, *args, **kwargs):
        """
        :type healthCheckNotification: bool
        :type instance: list[Instance]
        :type ipAddressResourceId: list[int]
        :type loadBalancerClassOfServiceID: int
        :type name: str
        :type notificationContacts: NotificationContacts or list[NotificationContact]
        :type rules: Rules
        :param healthCheckNotification: Enable or disable notifications
        :param instance: List of balanced IP Addresses (VM or server)
        :param ipAddressResourceId: ID of the IP Address resource of the Load Balancer
        :param loadBalancerClassOfServiceID: default 1
        :param name: Name of the Load Balancer
        :param notificationContacts: Nullable if notificationContacts is false
        :param rules: List of NewLoadBalancerRule object containing the list of rules to be configured with the service
        """
        response = self._call(method=SetEnqueueLoadBalancerCreation,
                              healthCheckNotification=healthCheckNotification,
                              instance=instance,
                              ipAddressResourceId=ipAddressResourceId,
                              name=name,
                              notificationContacts=notificationContacts,
                              rules=rules,
                              loadBalancerClassOfServiceID=loadBalancerClassOfServiceID,
                              *args, **kwargs)

    def get(self):
        """
        Get the current active and inactive Load Balancer within the Datacenter
        :return: (list) List of each LoadBalancer present in the Datacenter
        """
        return self._call(GetLoadBalancers)

    def get_notifications(self, startDate, endDate, loadBalancerID, loadBalancerRuleID):
        """
        Get the load balancer notifications for a specific rule within a specifying window time frame
        :type startDate: datetime
        :type endDate: datetime
        :type loadBalancerID: int
        :type loadBalancerRuleID: int
        :param startDate: From Date
        :param endDate: To Date
        :param loadBalancerID: ID of the Laod Balancer
        :param loadBalancerRuleID: ID of the Load Balancer Rule
        """
        return self._call(GetLoadBalancerNotifications, startDate=startDate, endDate=endDate,
                          loadBalancerID=loadBalancerID, loadBalancerRuleID=loadBalancerRuleID)

    def start(self, loadBalancerID):
        """
        Start a Load Balancer instance
        :type loadBalancerID: int
        :param loadBalancerID: ID of the Load Balancer to start
        :return:
        """
        return self._call(SetEnqueueLoadBalancerStart, loadBalancerID=loadBalancerID)

    def stop(self, loadBalancerID):
        """
        Stop a Load Balancer instance
        :type loadBalancerID: int
        :param loadBalancerID: ID of the Load Balancer to stop
        :return:
        """
        return self._call(SetEnqueueLoadBalancerPowerOff, loadBalancerID=loadBalancerID)

    def delete(self, loadBalancerID):
        """
        Enqueue a Load Balancer Deletion action
        :type loadBalancerID: int
        :param loadBalancerID: ID of the Load Balancer to be deleted
        :return:
        """
        return self._call(SetEnqueueLoadBalancerDeletion, loadBalancerID=loadBalancerID)
