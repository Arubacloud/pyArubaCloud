from LoadBalancerAlgorithmType import LoadBalancerAlgorithmType
from LoadBalancerProtocol import LoadBalancerProtocol


class NewLoadBalancerRule(object):
    def __init__(self, balancerType, certificate, creationDate, id, instancePort, loadBalancerPort, protocol):
        """
        :type balancerType: LoadBalancerAlgorithmType
        :type certificate: str
        :type creationDate: datetime
        :type id: int
        :type instancePort: int
        :type loadBalancerPort: int
        :type protocol: LoadBalancerProtocol
        :param balancerType:
        :param certificate:
        :param creationDate:
        :param id:
        :param instancePort:
        :param loadBalancerPort:
        :param protocol:
        """
        self.BalancerType = balancerType
        self.Certificate = certificate
        self.CreationDate = creationDate
        self.ID = id
        self.InstancePort = instancePort
        self.LoadBalancerPort = loadBalancerPort
        self.Protocol = protocol
