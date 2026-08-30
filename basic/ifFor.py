# if / for
score = 85

if score >= 90:
    print('优秀')
elif score >= 60:
    print('及格')
else:
    print('不及格')
    
users = ['Tom', 'Jack', 'Lucy']

for user in users:
    print(user)
    
user = {
    'name': 'Tom',
    'age': 20
}

# 遍历key
for key in user:
    print(key)
    
# 遍历key和value
for key, value in user.items():
    print(key, value)
    
# range
# 如果你想循环指定次数：
for i in range(5):
    print(i)
    
# 推导式
# [
#     我要什么
#     for 从哪里取数据
#     if 满足什么条件
# ]
result = [user.upper() for user in users]

result = [
    user
    for user in users
    if user != 'Jack'
]