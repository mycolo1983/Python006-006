import time
def timer(func):
    def inner(*args, **kwargs):
        beginTime = time.time()
        print(f'函数开始时间:{beginTime}')
        ret = func(*args, **kwargs)
        endTime = time.time()
        print(f'函数结束时间:{endTime}')
        print(f'函数的计算时间是:{endTime - beginTime}')
        return ret

    return inner


@timer
def my_count(b):
    a = 0
    for i in range(b):
        a += i
    return f"1到{b}累计的和={a}"


count1 = my_count(10)
print(count1)
