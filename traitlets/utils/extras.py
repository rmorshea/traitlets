import functools
from ..traitlets import DefaultHandler


def go_between(public, proxy):
    return GoBetween(public, proxy)


class GoBetween(DefaultHandler):

    def __init__(self, public, proxy):
        super(GoBetween, self).__init__(public)
        self.proxy = proxy

    def _init_call(self, func):
        @functools.wraps(func)
        def wrapper(owner):
            if not hasattr(owner, self.proxy):
                default = getattr(type(owner), self.trait_name).default()
                setattr(owner, self.proxy, default)
            return func(owner)
        self.func = wrapper
        return self

    def instance_init(self, obj):
        obj.observe(self._reset, self.trait_name, "change")
        obj.observe(self._reset, self.trait_name, "default")

    def _reset(self, data):
        try:
            del data.owner._trait_values[data.name]
        except:
            pass
        else:
            if hasattr(data, "new"):
                setattr(data.owner, self.proxy, data.new)
