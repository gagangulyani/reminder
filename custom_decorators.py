import functools


def validate_type(func):
    @functools.wraps(func)
    def wrap(*arg, **kwargs):
        if type(arg[0]) != type(arg[1]):
            raise TypeError(
                f"cannot compare instances of \"{arg[0].__class__.__name__}\" and \"{arg[1].__class__.__name__}\""
            )
        return func(*arg, **kwargs)
    return wrap
