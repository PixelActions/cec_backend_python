class Entity(object):
    def __init__(self, cid, created_on, name='',extra=''):
        self.cid = cid
        self.created_on = created_on
        self.name=name
        self.extra=extra
    def __unicode__(self):
        return self.cid

class Generator(object):
    def __init__(self, id, created_on, name='', **kwargs):
        self.id = cid
        self.created_on = created_on
        self.name=name
    def __unicode__(self):
        return self.name
class Test(object):
    def __init__(self, id, created_on, entity, **kwargs):
        self.id = id
        self.created_on = created_on
        self.entity=entity
        for key,val in kwargs.items():
            setattr(self, key, val)

    def __unicode__(self):
        return self.id
