from NewLoadBalancerRule import NewLoadBalancerRule


class Rules(list):
    def __init__(self, *args, **kwargs):
        super(Rules, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        assert isinstance(value, NewLoadBalancerRule), Exception(
            'Expected NewLoadBalancerRule, got: {}'.format(type(value)))
        super(Rules, self).__setitem__(key, value)

    def __str__(self):
        super(Rules, self).__str__()

    def append(self, p_object):
        assert isinstance(p_object, NewLoadBalancerRule), Exception(
            'Expected NewLoadBalancerRule, got: {}'.format(type(p_object)))
        super(Rules, self).append(p_object)

    def insert(self, index, p_object):
        assert isinstance(p_object, NewLoadBalancerRule), Exception(
            'Expected NewLoadBalancerRule, got: {}'.format(type(p_object)))
        super(Rules, self).insert(index, p_object)
