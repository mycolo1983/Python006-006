def mymap(func, iterator):
    return (func(it) for it in iterator)

def func(x):
    return x **2

for i in mymap(func, range(10)):
    print(i)
