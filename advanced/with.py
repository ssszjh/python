# Python 上下文管理器 with
# with 本质上就是 Python 提供的一套资源管理机制。

with
 ↓
__enter__()
 ↓
执行 with 里面的代码
 ↓
__exit__()

1.
class Test:
    def __enter__(self):
        print('enter')

    def __exit__(self, exc_type, exc_value, traceback):
        print('exit')


with Test():
    print('hello')
    
enter hello exit

2.
__exit__() 只有在 with 里面没有异常时才会执行。
错；都会执行

3.
with Test():
    print('hello')
① _______enter___
② 执行 print('hello')
③ _____exit_____

4.
class Test:
    def __enter__(self):
        print('enter')

    def __exit__(self, exc_type, exc_value, traceback):
        print('exit')


with Test():
    print('hello')
    1 / 0
会

with xxx as x 中的 x，就是 __enter__() 的返回值。
__enter__()
   ↓
返回一个对象
   ↓
as x
   ↓
x 得到这个对象

5.
class Test:
    def __enter__(self):
        return 'hello'

    def __exit__(self, exc_type, exc_value, traceback):
        print('exit')


with Test() as x:
    print(x)
hello exit

6.
def __enter__(self):
    return 123
with Test() as x:
x为123

7.as x 中的 x 是 Test() 对象本身
x是__enter__()的返回值

def __exit__(self, exc_type, exc_value, traceback):
这三个参数用来告诉 __exit__：with 里面有没有发生异常？如果有，是什么异常？
exc_type
↓
“什么类型的异常？”

exc_value
↓
“异常具体是什么？”

traceback
↓
“异常发生在哪里？”

exc_type
↓
“什么类型的异常？”

exc_value
↓
“异常具体是什么？”

traceback
↓
“异常发生在哪里？”

没有异常：
exc_type  = None
exc_value = None
traceback = None

有异常：
exc_type  = 异常类型
exc_value = 异常对象/异常信息
traceback = 异常追踪信息

8.
class Test:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        print(exc_type)
        print(exc_value)


with Test():
    print('hello')

exc_type = None
exc_value = None

9.
with Test():
    1 / 0
exc_type ≈ ?
exc_value ≈ ?
<class 'ZeroDivisionError'>
division by zero

10.
__exit__ 的三个参数，是用来接收 with 代码块产生的异常信息的
对


1 / 0
 ↓
ZeroDivisionError
 ↓
__exit__()
 ↓
return True
 ↓
异常被吞掉
 ↓
继续执行 with 后面的代码
 ↓
after


return True
    ↓
异常被处理，不继续抛

return False / None
    ↓
异常继续向外抛

__exit__() 返回 True → 吞掉异常

__exit__() 返回 False / None → 异常继续抛出

11.
class Test:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return True


with Test():
    1 / 0

print('after')
不会报 ZeroDivisionError;因为true 异常被吞掉了

12.
def __exit__(self, exc_type, exc_value, traceback):
    return False
print('after')
after不会执行 异常抛出

13.
def __exit__(self, exc_type, exc_value, traceback):
    return True
  
with Test():
    print('hello')
正常执行；hello

                Test()
                  ↓
             __enter__()
                  ↓
             返回值 → x
                  ↓
            执行 with 代码
                  ↓
          ┌───────┴───────┐
          ↓               ↓
       无异常            有异常
          ↓               ↓
 __exit__(None...)   __exit__(异常信息)
          ↓               ↓
        结束       ┌───────┴───────┐
                   ↓               ↓
                 True          False / None
                   ↓               ↓
                吞掉异常        继续抛出
                
14.
class Test:
    def __enter__(self):
        print('A')
        return 100

    def __exit__(self, exc_type, exc_value, traceback):
        print('C')
        print(exc_type)
        return True


with Test() as x:
    print('B', x)
    1 / 0

print('D')

A B 100 C ZeroDivisionError D

# contextlib

@contextmanager
       ↓
   yield 前
       ↓
   进入 with
       ↓
     yield
       ↓
   执行 with 内部
       ↓
   yield 后
       ↓
   离开 with
   
15.
from contextlib import contextmanager

@contextmanager
def test():
    print('A')
    yield
    print('C')


with test():
    print('B')
  
A B C

16.
@contextmanager
def test():
    print('A')
    yield 100
    print('C')


with test() as x:
    print('B', x)

A B,100 C

普通上下文管理器             @contextmanager

__enter__()        ≈         yield 前面的代码
      ↓                         ↓
with 内部代码                  with 内部代码
      ↓                         ↓
__exit__()         ≈         yield 后面的代码

17.
@contextmanager
def test():
    print('A')
    yield
    print('C')
    
with test():
    print('B')
    1 / 0

A B C不会执行 ZeroDivisionError会抛出

计时器
import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()

    yield

    end = time.time()
    print('耗时:', end - start)
    
with timer():
    time.sleep(2)
    
contextmanager 函数
       ↓
执行 yield 前代码
       ↓
yield
       ↓
暂停
       ↓
Python 去执行 with 代码
       ↓
with 代码结束
       ↓
恢复 contextmanager
       ↓
执行 yield 后代码

18.
@contextmanager
def test():
    print('1')
    yield
    print('3')


with test():
    print('2')
    
为什么输出1 2 3
因为contextmanager首先执行yield前的代码
然后再自己执行with里的代码
最后执行yield后的代码

19.
@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(end - start)

yield 前面的代码和 yield 后面的代码分别负责什么？
yield 前面的代码记录开始时间
yield 后面的代码记录结束时间

20.
yield 执行后，会立刻执行 yield 后面的代码。
错；要执行with里代码先，才执行yield后的代码

21.
from contextlib import contextmanager

@contextmanager
def test():
    print('A')

    try:
        yield
    finally:
        print('C')


with test():
    print('B')
    1 / 0

print('D')

A → B → C → ZeroDivisionError

finally：我不管你有没有异常，我先把清理工作做完。

__exit__ 返回 True：这个异常我处理了，别再往外抛


with
├── __enter__()
├── __exit__()
│   ├── exc_type
│   ├── exc_value
│   └── traceback
│
├── as x
│   └── x = __enter__() 返回值
│
└── __exit__ 返回 True
    └── 吞掉异常
    
@contextmanager
├── yield 前
│   └── 进入阶段
│
├── yield
│   └── 把控制权交给 with
│
└── yield 后 / finally
    └── 退出阶段