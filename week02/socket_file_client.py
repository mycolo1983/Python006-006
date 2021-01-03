#! /usr/bin/env python3
import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
# 每次发送4096个字节
BUFFER_SIZE = 1024

# 指定服务器IP、端口和要发送文件的名字
HOST = 'localhost'
PORT = 5001
FILENAME = 'vm.bundle'

# 以字节为单位获取文件大小，打印进度条使用
filesize = os.path.getsize(FILENAME)
print(filesize)

# 创建socket套接字,AF_INET:IPv4地址,SOCK_STREAM:TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
print(f"[+] Connecting to {HOST}:{PORT}")
s.connect((HOST,PORT))
print(f"[+] Connected.")

# 发送文件名和文件大小,这里使用了分隔符SEPARATOR来分隔数据字段，也可以使用两次send来达到同样的效果
# 要求发送的字符串格式必须是binary类型，所以使用encode()方法将utf-8类型转换成binary类型
s.send(f"{FILENAME}{SEPARATOR}{filesize}".encode())

# 发送文件，并打印进度条
progress = tqdm.tqdm(range(filesize), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
with open(FILENAME, "rb") as f:
    for _ in progress:
        # 从文件中读取字节
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # 文件传输完成
            break
        # 使用sendall来传输
        s.sendall(bytes_read)
        # 更新进度条
        progress.update(len(bytes_read))
# 关闭套接字
s.close()
