import functools

def fun(fun1):
    @functools.wraps(fun1)
    def decorator(*argv):
        print('===')
        fun1(*argv)
        print('===')
    return decorator

@fun
def print_fun(msg, msg2):
    print('hello ' + msg + msg2)


print(print_fun.__name__)