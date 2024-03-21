from functools import wraps


from pysplainer.tracer import trace_function


def explainable(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "explainable" in kwargs and kwargs["explainable"] == True:
            del kwargs["explainable"]
            return trace_function(func, *args, **kwargs)

        return func(*args, **kwargs)

    return wrapper
