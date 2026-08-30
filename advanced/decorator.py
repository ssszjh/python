# 装饰器
# 装饰器的本质
# 函数
# +
# 闭包
# +
# *args
# +
# **kwargs

def log(func):

    def wrapper(*args, **kwargs):
        print('开始执行')
        result = func(*args, **kwargs)
        print('执行结束')
        return result

    return wrapper

@log
def add(a, b):
    return a + b
add(1, 2)

# 开始执行
# 执行结束
# 返回3
# @log等价于add = log(add)

1.
def log(func):
    def wrapper():
        print('before')
        func()
        print('after')

    return wrapper


def hello():
    print('hello')


hello = log(hello)

hello()
# before
# hello
# after

2.
hello = log(hello)
# 执行以后，hello 还是原来的 hello 函数吗？
# 不是;是log里的wrapper

3.
def log(func):
    def wrapper():
        print('before')
        result = func()
        print('after')
        return result

    return wrapper


@log
def hello():
    return 'hello'


print(hello())
# before
# hello
# after

4.
def log(func):
    def wrapper():
        print('before')
        return func()

    return wrapper


@log
def add(a, b):
    return a + b


print(add(1, 2))
# 会发生什么？
# 提示：wrapper 没有接收参数。
# before
# none