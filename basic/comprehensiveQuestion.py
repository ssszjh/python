users = [
    {'name': 'Jack', 'age': 20, 'role': 'admin'},
    {'name': 'Tom', 'age': 17, 'role': 'user'},
    {'name': 'Lucy', 'age': 25, 'role': 'user'},
    {'name': 'Bob', 'age': 30, 'role': 'admin'},
]
# 找出年龄 ≥ 18，并且 role == 'admin' 的用户，只返回名字。
# 结果
[
    'Jack',
    'Bob'
]

resule = [ user['name'] for user in users if user['role'] == 'admin' and user['age'] >= 18]

users = [
    {'name': 'Jack', 'age': 20},
    {'name': 'Tom', 'age': 17},
    {'name': 'Jack', 'age': 25},
    {'name': 'Lucy', 'age': 30},
    {'name': 'Tom', 'age': 22}
]
{
    'adult_count': 4,
    'names': ['Jack', 'Tom', 'Lucy']
}

# adult_count：年龄 ≥ 18 的用户数量
# names：所有成年人的名字，去重
# names 必须是 list
# 保持第一次出现的顺序

result = {
    'adult_count': 0,
    'names': []
}

for user in users:
    if user['age'] >= 18:
        result['adult_count'] += 1

        if user['name'] not in result['names']:
            result['names'].append(user['name'])