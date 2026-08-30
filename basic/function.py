# 函数
def greet(name, message='Hello'):
    print(message, name)

greet('Jack')
greet('Tom', 'Hi')

def add(a, b):
    result = a + b

print(add(1, 2))


def add_user(name, users=[]):
    users.append(name)
    return users


print(add_user('Jack')) #['Jack']
print(add_user('Tom')) #['Jack', 'Tom']
print(add_user('Lucy')) #['Jack', 'Tom', 'Lucy']

def get_user():
    pass


user = get_user()

if user:
    print('有用户')
else:
    print('没有用户')
    
# 没有用户 
# pass 的意思非常简单：
# 什么都不做，占位。
# 因为没有 return 函数返回none 
