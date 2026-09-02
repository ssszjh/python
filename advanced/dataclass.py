# dataclass

class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

user = User('Jack', 20, 'jack@test.com')

# 等价于下面

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str
    
user = User('Jack', 20, 'jack@test.com')

# 不需要自己写
# def __init__(...):

# 帮你自动处理
# __init__
# __repr__
# __eq__

# 创建对象
#    ↓
# 方便打印
#    ↓
# 方便比较

# 默认值
@dataclass
class User:
    name: str
    age: int = 18
    
    
# 默认值 + 可变对象
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    tags: list = field(default_factory=list)

# 这样每个 User 都会得到自己的 list。

# 是一个带有大量自动生成样板代码能力的 class

# | Python                        | TypeScript          | 作用            |
# | ----------------------------- | ------------------- | ------------- |
# | `class`                       | `class`             | 创建真正的对象       |
# | `@dataclass`                  | 没有完全对应物             | 减少 class 样板代码 |
# | `str` / `int`                 | `string` / `number` | 类型注解          |
# | `__init__`                    | `constructor`       | 初始化           |
# | `__repr__`                    | 类似调试字符串             | 打印对象          |
# | `__eq__`                      | 类似自定义比较             | 对象相等判断        |
# | `field(default_factory=list)` | 类似安全的默认工厂           | 每个实例独立对象      |

1.
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

user = User('Jack', 20)

print(user)
User(name='Jack', age=20)

2.
@dataclass
class User:
    name: str
    age: int = 18
   
u1 = User('Jack')
u2 = User('Tom', 20)

print(u1.age)
print(u2.age) 
# 18 20

3.
@dataclass
class User:
    name: str
    age: int

u1 = User('Jack', 20)
u2 = User('Jack', 20)

print(u1 == u2)
# true; dataclass 做了__eq__；会根据字段进行比较

4.
# 下面哪个更推荐？
# A
@dataclass
class User:
    tags: list = []
# B
@dataclass
class User:
    tags: list = field(default_factory=list)

# 推荐B ;因为list是可变对象；default_factory为类似安全的默认工厂
# 写法 A：tags: list = []
# 这里的 [] 在定义类时（而不是实例化时）只被创建一次。所有不传 tags 参数的 User 实例，它们的 tags 属性都指向内存中的同一个列表对象。
# 写法 B：tags: list = field(default_factory=list)
# default_factory=list 表示每次实例化类时，都会调用 list() 构造函数创建一个全新的空列表。每个实例拥有自己独立的内存空间。


5.
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int = 18
    tags: list = field(default_factory=list)

u1 = User('Jack')
u2 = User('Tom', 20)

u1.tags.append('python')

print(u1)
print(u2)
# User(name='Jack', age=18, tags=['python'])
# User(name='Tom', age=20)


from dataclasses import dataclass, field

# 希望某个字段不允许用户创建对象时传入
# field(init=False)
# 字段不要放进自动生成的 __init__() 参数里
@dataclass
class User:
    name: str
    age: int
    id: int = field(init=False)
    
# 可以在 __post_init__() 里处理
# from dataclasses import dataclass, field

# @dataclass
# class User:
#     name: str
#     age: int
#     id: int = field(init=False)

#     def __post_init__(self):
#         self.id = 100
# 不允许用户创建对象时传入的属性

# User('Jack', 20)
#        ↓
# __init__()
#        ↓
# name = Jack
# age = 20
#        ↓
# __post_init__()
#        ↓
# id = 100

frozen=True
# 创建之后，不允许修改字段
# 可以把它暂时理解成一个“只读对象”
@dataclass(frozen=True)
class User:
    name: str
    age: int
    
6.
@dataclass
class User:
    name: str
    id: int = field(init=False)
# A. User('Jack', 100)
# B. User('Jack')
# B

7.
@dataclass
class User:
    name: str
    id: int = field(init=False)

    def __post_init__(self):
        self.id = 100

user = User('Jack')
print(user)
User(name='Jack', id=100)

8.
@dataclass(frozen=True)
class User:
    name: str
    age: int

user = User('Jack', 20)
user.age = 30
# 报错；frozen冻结，不可修改

9.
@dataclass(frozen=True)
class User:
    tags: list = field(default_factory=list)
# frozen=True 是否意味着 user.tags 这个 list 里面的元素也完全不能修改
# 可以修改
# user.tags = [] 不允许
# user.tags.append('python') 允许
# 因为 frozen=True 主要限制的是：
# 不能重新给字段赋值

# frozen=True 让 dataclass 实例的字段不能被重新赋值，但字段引用的可变对象本身仍可能被修改。

# species
# 这是类级别的数据，不是每个实例自己的字段。
from typing import ClassVar

@dataclass
class User:
    name: str
    age: int

    species: ClassVar[str] = 'human'
# 这样 species 就不会参与 dataclass 的 __init__、repr、eq 等字段处理。

# @dataclass
#    │
#    ├── 自动生成 __init__
#    ├── 自动生成 __repr__
#    ├── 自动生成 __eq__
#    │
#    ├── 默认值
#    │
#    ├── field()
#    │    ├── default_factory
#    │    └── init=False
#    │
#    ├── __post_init__()
#    │
#    ├── frozen=True
#    │
#    └── ClassVar