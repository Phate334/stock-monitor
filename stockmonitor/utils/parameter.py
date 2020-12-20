def func_helper(parameter_type, return_type=None):
    def decorator(function):
        def wrapper(self, **kwargs):
            result = function(self, parameter_type(**kwargs))
            return return_type(**result) if return_type else result

        return wrapper

    return decorator
