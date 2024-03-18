from functools import wraps


from pysplainer.tracer import trace_function


def explainable(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "explain" in kwargs and kwargs["explain"] == True:
            del kwargs["explain"]
            return trace_function(func, *args, **kwargs)

        return func(*args, **kwargs)

    return wrapper
