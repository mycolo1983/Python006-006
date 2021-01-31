import redis
import time

client = redis.Redis(host='mysqlsev1',password='hUN7e4_1')

def sendsms(telephone_number, content, key=None):
   
    if not client.get(telephone_number):
        client.set(telephone_number, 1, 60, nx=True)
        print('发送成功1')

    elif int(client.get(telephone_number).decode()) < 5:
        try:
            client.incr(telephone_number)
            print('发送成功2')
        except Exception as e:
            print(e)

    else:
        print('1 分钟内发送次数超过 5 次, 请等待 1 分钟')
        #sleep(60)


if __name__ == '__main__':
    sendsms(12345654321, content="hello")  # 发送成功
    sendsms(12345654321, content="hello")  # 发送成功
    sendsms(88887777666, content="hello")  # 发送成功
    sendsms(12345654321, content="hello")  # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
    sendsms(88887777666, content="hello")  # 发送成功
