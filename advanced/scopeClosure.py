# 作用域
# 闭包

# 局部变量
# 全局变量
# LEGB
# global
# nonlocal
# 闭包

# 作用域
1.
x = 10

def test():
    x = 20
    print(x)

test()
print(x)
# 20 10

2.
x = 10

def test():
    print(x)

test()
# 函数里面没有自己的 x，所以会向外找。
# 10

3.
x = 10

def test():
    x += 1
    print(x)

test()
# 报错;test的x未定义就操作
# Python 发现函数里有 x += 1，因此把 x 判断为局部变量，但在读取它进行 + 1 时，这个局部变量还没有初始化

4.
def outer():
    x = 10

    def inner():
        print(x)

    inner()

outer()
# 10

5.
def outer():
    x = 10

    def inner():
        x = 20
        print(x)

    inner()
    print(x)

outer()
# 20 10

# Python 变量查找规则
# L → Local
# E → Enclosing
# G → Global
# B → Built-in
# Local 当前函数
#  ↓
# Enclosing 外层函数
#  ↓
# Global 全局
#  ↓
# Built-in py内置

# nonlocal
def counter():
    count = 0

    def add():
        nonlocal count
        count += 1
        
# count
# 不是 add 的 Local
# 不是 Global
# 而是 outer 的变量
# 我要修改外层函数的 count，而不是在当前函数创建一个新的 count

# global nonlocal
# global
# ↓
# 修改全局变量

# nonlocal
# ↓
# 修改外层函数变量

1.
x = 10

def outer():
    x = 20

    def inner():
        print(x)

    inner()

outer()
# 20


2.
x = 10

def outer():
    x = 20

    def inner():
        x = 30
        print(x)

    inner()
    print(x)

outer()
print(x)
# 30 20 10


3.
x = 10

def outer():
    x = 20

    def inner():
        nonlocal x
        x = 30

    inner()
    print(x)

outer()
print(x)
# 30 10

4.
def counter():
    count = 0

    def add():
        nonlocal count
        count += 1
        return count

    return add


c1 = counter()
c2 = counter()

print(c1())
print(c1())
print(c2())
print(c1())
# 1 2 1 3
# c1 和 c2 不共用同一个 count。

5.
def counter():
    count = 0

    def add():
        count += 1
        return count

    return add


c = counter()

print(c())
# 报错 count未定义就执行


6.
def create_multiplier(n):
    def inner(m):
        return n*m

    return inner
    
double = create_multiplier(2)
triple = create_multiplier(3)

print(double(10))
print(triple(10))
# 输出 20 30

# 闭包
# 内部函数引用了外部函数的变量，并且外部函数执行结束后，这些变量仍然被内部函数保留。