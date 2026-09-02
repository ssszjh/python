# lambda 基本格式
# 什么需要 lambda？
# 因为有时候一个函数只用一次。
# lambda 参数: 返回值

def get_age(user):
    return user['age']

# 等价于
lambda user: user['age']

# 调用
print((lambda x: x * 2)(10))

# sort()
users = [
    {'name': 'Jack', 'age': 30},
    {'name': 'Tom', 'age': 18},
    {'name': 'Lucy', 'age': 25}
]
users.sort(key=lambda user: user['age'])
# 它会直接修改原来的 list。

# sorted()
result = sorted(
    users,
    key=lambda user: user['age']
)
# 返回一个新的 list，不修改原来的 users。

# 默认从小到大
# 若要从大到小
# reverse=True
users.sort(
    key=lambda user: user['age'],
    reverse=True
)

# map
names = list(
    map(lambda user: user['name'], users)
)

# filter
adults = list(
    filter(lambda user: user['age'] >= 18, users)
)

# lambda
# ↓
# 一个简单的匿名函数

# sort
# ↓
# 修改原 list

# sorted
# ↓
# 返回新的 list

# map
# ↓
# 每个元素转换一下

# filter
# ↓
# 筛选元素

# 列表推导式
# ↓
# Python 中非常常用的数据处理方式

1.
add = lambda x, y: x + y

print(add(10, 20))
# 30

2.
users = [
    {'name': 'Jack', 'age': 30},
    {'name': 'Tom', 'age': 18},
    {'name': 'Lucy', 'age': 25}
]

users.sort(key=lambda user: user['age'])

print(users)
# [
#     {'name': 'Tom', 'age': 18},
#     {'name': 'Lucy', 'age': 25},
#      {'name': 'Jack', 'age': 30}
# ]

3.
result1 = users.sort(
    key=lambda user: user['age']
)

result2 = sorted(
    users,
    key=lambda user: user['age']
)
# result1 和 result2 分别是什么？
# result1会改变users; result2 不会

4.
# 使用map
users = [
    {'name': 'Jack', 'age': 20},
    {'name': 'Tom', 'age': 18},
    {'name': 'Lucy', 'age': 25}
]
# 得到：
['Jack', 'Tom', 'Lucy']
result = list.map(lambda user: user['name'], users)

5.
# 使用filter
users = [
    {'name': 'Jack', 'age': 20},
    {'name': 'Tom', 'age': 17},
    {'name': 'Lucy', 'age': 25}
]
# 得到成年人
result = list.filter(lambda user: user['age'] >=18, users)

6.
users = [
    {'name': 'Jack', 'age': 30, 'score': 80},
    {'name': 'Tom', 'age': 17, 'score': 95},
    {'name': 'Lucy', 'age': 25, 'score': 90},
    {'name': 'Bob', 'age': 20, 'score': 70}
]
# 找出年龄 ≥ 18 且成绩 ≥ 80 的用户，然后按照成绩从高到低排序，最后只返回名字。
people = [
    user
    for user in users
    if user['age'] >= 18 and user['score'] >= 80
]

people.sort(
    key=lambda user: user['score'],
    reverse=True
)

result = [
    user['name']
    for user in people
]