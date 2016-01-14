class Template(object):
    descr = None
    template_id = ''
    id_code = None
    hypervisor = None
    name = None
    enabled = None

    class ResourceBounds(object):
        def __init__(self):
            self.max_cpu = None
            self.max_memory = None
            self.hdd0 = None
            self.hdd1 = None
            self.hdd2 = None
            self.hdd3 = None

    def __init__(self, hypervisor):
        self.hypervisor = hypervisor
        self.resource_bounds = self.ResourceBounds()

    def __str__(self):
        msg = 'Template Name: %s\n' % self.descr
        msg += ' -> Hypervisor: %s\n' % self.hypervisor
        msg += ' -> IdCode: %s\n' % self.id_code
        msg += ' -> Id: %s\n' % self.template_id
        msg += ' -> Enabled: %s\n' % self.enabled
        return msg

    def __repr__(self):
        return 'Template Name: %s, Hypervisor: %s, Id: %s, Enabled: %s' % (
            self.descr, self.hypervisor, self.template_id, self.enabled
        )
