# *args / **kwargs
# *args：接收任意数量的位置参数
# args 本身是一个 tuple（元组）
# **kwargs：接收任意数量的关键字参数
# kwargs 是一个 dict。
# *args
# ↓
# 多个位置参数
# ↓
# tuple

# **kwargs
# ↓
# 多个关键字参数
# ↓
# dict

# * 不只是定义时有用
# 拆包
numbers = [1, 2, 3]
print(*numbers)
# 1 2 3

user = {
    'name': 'Jack',
    'age': 20
}

def test(name, age):
    print(name, age)

test(**user)
相当于
test(
    name='Jack',
    age=20
)

1.
def test(*args):
    print(args)

test(1, 2, 3)
# (1,2,3)

2.kwargs 是什么类型
def test(**kwargs):
    print(kwargs)

test(name='Jack', age=20)
# {
#   name: 'Jack',
#   age: 20
# }

3.
def test(*args, **kwargs):
    print(args) #(1,2)
    print(kwargs)
#     {
#   name: 'Jack',
#   age: 20
# }

test(1, 2, name='Jack', age=20)

4.拆包
def test(name, age):
    print(name, age)
    # jack 20

user = {
    'name': 'Jack',
    'age': 20
}

test(**user)

5.
# 也就是说，不管传多少个数字，都计算总和
def add(*args):
    total = 0

    for num in args:
        total += num

    return total
  
add(1, 2, 3)
# 6

add(10, 20, 30, 40)
# 100
6.
def print_user(**kwargs):
    for key, value in kwargs.items():
        print(f'{key}: {value}')
    
print_user(name='Jack', age=20, city='Beijing')
# name: Jack
# age: 20
# city: Beijing