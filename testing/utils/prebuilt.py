def prebuild(self, func):
    def inner(*args, **kwargs):
        func(self, *tuple(args), **kwargs)
        
    return inner