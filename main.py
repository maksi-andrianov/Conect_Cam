import socket
import sys
import json
from datetime import datetime


def conect_cam():
    HOST, PORT = "192.168.1.79", 55256

    # m ='{"id": 2, "name": "abc"}'
    m = "23" "{\"ACK\":\"\",\"RET\":0}\n\u0003r"  # словарь из лог файла программы DATA MATRIX HONEYWELL

    data = json.dumps(m)

    # Create a socket (SOCK_STREAM means a TCP socket WINDOWS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Содаём подключение....')

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        connected = True
        print('Камера подключена')
        sock.sendall(bytes(data, encoding="utf-8"))
        print('Сообщение на камеру отправлено')
        data_out = {'code_id': '', 'create_date': ''}
        while True:
            # Receive data from the server and shut down
            received = sock.recv(1024)
            print('Тип recived', type(received))
            received = received.decode("utf-8")
            #received = received.split('\\')
            time_resiev = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print("Sent:     {}".format(data))
            print("Received: {}".format(received))
            print("Received: {}",(received))
            print(time_resiev)
            print('Тип recived',type(received))

            data_out.update({'code_id':received[:-7], 'create_date':time_resiev})
            filename = datetime.now().strftime('%Y-%m-%d')
            print('data_out',data_out)
            with open(str(filename) + '.json', 'a') as out_file:
                json.dump((data_out), out_file, sort_keys=True, indent=0, ensure_ascii=False)
                #json.dumps(format(data_out), out_file, indent=6)
                #print(type(out_file))
                #out_file.write('out_data')
                out_file.write(',')

            # out_file.write(format(received) +'\n')
            # for  line in json.dump(format(received)):
            # file.write(line + '\n')

            # received = sock.recv(1024)
            # received = received.decode("utf-8")


    # finaly:
    except:


        # print ("Received: {}".format(received))
        print('Ошибка связи')
        sock.close()
        print('Подкючение закрыто')

def reconect_cam():
    connected = False
    while not connected:
        conect_cam()

def valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


conect_cam()
if __name__ == '__main__':
    conect_cam()
    reconect_cam()


