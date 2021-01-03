#! /usr/bin/env python3
import socket
import tqdm
import os
# 服务端的IP和地址，确保和客户端使用的一样的端口
HOST = 'localhost'
PORT = 5001
# 每次接收4096个字节
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

# 创建socket套接字,AF_INET:IPv4地址,SOCK_STREAM:TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 将套接字对象s绑定到指定的主机和端口上
s.bind((HOST,PORT))

# 监听连接。listen()中的数字表示系统在拒绝新连接之前允许的未接受连接的数量。listen(5)表示只接受5个连接
s.listen(5)
print(f"[*] Listening as {HOST}:{PORT}")

# accept表示接受用户端的连接
client_conn, client_addr = s.accept()

# 如果执行以下代码，则表示发送方已连接
print(f"[+] {client_addr} is connected.")

# 接收文件信息，使用client socket，非server socket
received= client_conn.recv(BUFFER_SIZE).decode()
filename,filesize=received.split(SEPARATOR)

# 去除绝对路径
filename='new_' + os.path.basename(filename)

# 转换为整数
filesize=int(filesize)

# 开始从套接字接收并写入文件
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        # 从套接字读取4096个字节
        bytes_read = client_conn.recv(BUFFER_SIZE)
        if not bytes_read:    
            break
        f.write(bytes_read)
        # 更新进度条
        progress.update(len(bytes_read))

# 关闭客户端套接字
client_conn.close()
# 关闭服务器套接字
s.close()