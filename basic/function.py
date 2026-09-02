# 函数
def greet(name, message='Hello'):
    print(message, name)

greet('Jack')
greet('Tom', 'Hi')

def add(a, b):
    result = a + b
    return result

print(add(1, 2))


def add_user(name, users=[]):
    users.append(name)
    return users


print(add_user('Jack')) #['Jack']
print(add_user('Tom')) #['Jack', 'Tom']
print(add_user('Lucy')) #['Jack', 'Tom', 'Lucy']
# 函数定义时，users=[] 这个空列表被创建一次，并作为默认值绑定到函数对象上。
# 每次调用时，如果不传入 users 实参，就会使用这个同一个列表对象（而不是每次新建一个空列表）。
# 因此，三次调用都在同一个列表上追加元素，导致输出累积
# 如何避免这个问题？
# 推荐做法：将默认值设为 None，在函数内部重新创建可变对象

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
