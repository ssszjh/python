# 可变对象 / 不可变对象
# 浅拷贝 / 深拷贝

# 不可变对象
#     ↓
# int / float / str / bool / tuple

# 可变对象
#     ↓
# list / dict / set

# 浅拷贝
#     ↓
# copy()

# 深拷贝
#     ↓
# deepcopy()

# 函数参数传递
#     ↓
# 为什么 Python 经常被说成“传对象引用”

# 变量名指向一个对象
# a = [1, 2, 3]
# a 不是“装着这个数组的盒子”，而是一个指向对象的名字。

# 不可变对象 → 修改通常意味着重新绑定
# 可变对象   → 可以直接修改原对象

# == → 值是否相等

# is → 是否是同一个对象

def add_item(items):
    items.append('Python')


users = ['Jack', 'Tom']

add_item(users)

print(users)
# ['Jack', 'Tom', 'Python']

# users
#  ↓
# list对象

# items
#  ↓
# 同一个list对象

      #               Python 对象
      #                  │
      #        ┌─────────┴─────────┐
      #        ↓                   ↓
      #     不可变                可变
      #        │                   │
      #  int / str / tuple    list / dict / set
      #        │                   │
      #  修改 → 重新绑定       可以直接修改
      #        │                   │
      #        └─────────┬─────────┘
      #                  ↓
      #            引用 / 复制
      #                  │
      #     ┌────────────┼────────────┐
      #     ↓            ↓            ↓
      #   b = a       a.copy()    deepcopy(a)
      #     │            │            │
      #   同一个        浅拷贝        深拷贝
      #   对象          第一层        递归复制
      
1.
a = [1, 2, 3]
b = a

b.append(4)

print(a)
print(b)
print(a is b)
# [1, 2, 3, 4]
# [1, 2, 3, 4]
# true

2.
a = [1, 2, 3]
b = a.copy()

b.append(4)

print(a)
print(b)
print(a is b)
# [1, 2, 3]
# [1, 2, 3, 4]
# false

3.
a = [[1, 2], [3, 4]]
b = a.copy()

b[0].append(100)

print(a)
print(b)
print(a is b)
print(a[0] is b[0])
# [[1, 2, 100], [3, 4]]
# [[1, 2, 100], [3, 4]]
# false
# true

4.
import copy

a = {
    'name': 'Jack',
    'info': {
        'age': 20
    }
}

b = copy.deepcopy(a)

b['info']['age'] = 30

print(a)
print(b)
# {
#     'name': 'Jack',
#     'info': {
#         'age': 20
#     }
# }
# {
#     'name': 'Jack',
#     'info': {
#         'age': 30
#     }
# }

5.
def test(data):
    data.append(4)


numbers = [1, 2, 3]

test(numbers)

print(numbers)
#  [1, 2, 3, 4]
# data 和 numbers 指向同一个 list。

6.
def test(data):
    data = data + [4]
    return data


numbers = [1, 2, 3]

result = test(numbers)

print(numbers)
print(result)
# numbers 是什么？
# result 是什么？
# 为什么这里和 data.append(4) 的结果不一样？
# [1, 2, 3]
# [1, 2, 3, 4]

# 修改原对象
# data.append(...)
# data.extend(...)
# data['xxx'] = ...

# 创建/得到一个新对象，然后重新让变量指向它
# data = data + ...
# data = data.copy()
# data = data[:]