from functools import wraps


def printer(fkn):
    @wraps(fkn)
    def wrapped(*args, **kwargs):
        res = fkn(*args, **kwargs)
        print(f"{fkn.__name__}(args: {args}", f"kwargs: {kwargs}) => {res}")
        return res

    return wrapped
