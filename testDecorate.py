def log(func):
    def weapper(*args,**kwargs):
        print('call %s():'%func.__name__)
        return func(*args,**kwargs)
    return weapper

