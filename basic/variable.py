# 变量

name = "Tom"
age = 18
height = 1.75
is_ok = True
data = None

print(type(name))
print(type(age))
print(type(height))
print(type(is_ok))
print(type(data))

# Python 判断一个变量是不是 xxx类型，用 isinstance()
# isinstance(value, xxx)

# Python 里 bool 是 int 的子类
isinstance(True, int)  # True
# issubclass(bool, int)  # True
# 所以如果你要严格判断整数，不包括 bool：
type(value) is int
# 表示判断 是不是整数或浮点数：
isinstance(x, (int, float))

a = 10
b = a
a = 20

print(a)
print(b)
# 20
# 10

a = [1, 2, 3]
b = a

b.append(4)

print(a)
print(b)
# [1, 2, 3, 4]
# [1, 2, 3, 4]

# 引用 vs 复制
a = {'name': 'Jack'}
b = a

b['name'] = 'Tom'

print(a) #{'name': 'Tom'}
print(b) #{'name': 'Tom'}

浅拷贝
a = {
    'name': 'Jack',
    'skills': ['Vue', 'React']
}

b = a.copy()

b['name'] = 'Tom'
b['skills'].append('Python')

print(a) 
# {
#     'name': 'Jack',
#     'skills': ['Vue', 'React', 'Python']
# }
print(b)
# {
#     'name': 'Tom',
#     'skills': ['Vue', 'React', 'Python']
# }

# == vs is
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b) #true
print(a is b) #false
# == 比较值
# is 比较同一个对象

a = {
    'user': {
        'name': 'Jack'
    }
}

b = a.copy()

b['user']['name'] = 'Tom'

print(a['user']['name']) #Tom
