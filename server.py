import socket as sk
import time


fields = [[], []]

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("127.0.0.1", 10666))
server.listen(2)
print('ON')

user1, adress1 = server.accept()
print('connected 1')
user2, adress2 = server.accept()
print('connected 2')

data = user1.recv(1024).decode('utf-8')
fields[0] = [list(map(int, data[i*10:i*10+10])) for i in range(10)]


data = user2.recv(1024).decode('utf-8')
fields[1] = [list(map(int, data[i*10:i*10+10])) for i in range(10)]

print('Preparation complited')
user1.send('1'.encode('utf-8'))
user2.send('2'.encode('utf-8'))
cnt = 1
while True:

    data1 = list(map(int, user1.recv(1024).decode("utf-8")))
    if fields[1][data1[0]][data1[1]] == 2:
        fields[1][data1[0]][data1[1]] = 3
        user1.send('3'.encode("utf-8"))
        user2.send(f'{data1[0]}{data1[1]}3'.encode('utf-8'))
    else:
        fields[1][data1[0]][data1[1]] = 1
        user1.send('1'.encode("utf-8"))
        user2.send(f'{data1[0]}{data1[1]}1'.encode('utf-8'))
    cnt1 = 0
    for i in fields[1]:
        cnt1 += i.count(2)
    cnt0 = 0
    for i in fields[0]:
        cnt0 += i.count(2)
    if not cnt1:
        user1.send('w'.encode('utf-8'))
        user2.send('l'.encode('utf-8'))
        break
    elif not cnt0:
        user1.send('l'.encode('utf-8'))
        user2.send('w'.encode('utf-8'))
        break

    data2 = list(map(int, user2.recv(1024).decode("utf-8")))
    if fields[0][data2[0]][data2[1]] == 2:
        fields[0][data2[0]][data2[1]] = 3
        user2.send('3'.encode("utf-8"))
        user1.send(f'{data2[0]}{data2[1]}3'.encode('utf-8'))
    else:
        fields[0][data2[0]][data2[1]] = 1
        user2.send('1'.encode("utf-8"))
        user1.send(f'{data2[0]}{data2[1]}1'.encode('utf-8'))
    cnt1 = 0
    for i in fields[1]:
        cnt1 += i.count(2)
    cnt0 = 0
    for i in fields[0]:
        cnt0 += i.count(2)
    if not cnt1:
        user1.send('w'.encode('utf-8'))
        user2.send('l'.encode('utf-8'))
        break
    elif not cnt0:
        user1.send('l'.encode('utf-8'))
        user2.send('w'.encode('utf-8'))
        break

    if not data1 or not data2:
        break

print('Finish')    
time.sleep(5)
server.close()