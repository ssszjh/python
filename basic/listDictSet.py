# list / dict / set
# list：列表 → 有顺序，可以重复
# dict：字典 → 键值对，通过 key 找 value
# set：集合 → 不重复，主要用来去重、集合运算

users = ["Tom", "Jack"]
users[0]
users.append("Lucy")
users.remove("Tom")
# 在下标 1 的位置插入。
# users.insert(1, 'Bob')

set 的集合运算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
# 交集
a & b 
# {3,4}
# 并集
a | b 
# {1, 2, 3, 4, 5, 6}
# 差集
# a 有、b 没有：
a - b
# {1, 2}


user = {
    'name': 'Jack',
    'age': 20
}

for key, value in user.items():
    print(key, value)
    
user.keys()
user.values()
user.items()

# keys() 拿 key
# values() 拿 value
# items() key-value 成对的数据