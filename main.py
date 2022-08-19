from threading import Thread
import time

def load_config():
    import configparser  # импортируем библиотеку
    print('Загружаем конфигурацию...')
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read('config.ini')
    print(config['CAM1']['IP'])
    IP_CAM1 = config['CAM1']['IP']
    print('ip_cam1',IP_CAM1)
    PORT = config['CAM1']['PORT']
    IP_CAM2 = config['CAM2']['IP']
    return IP_CAM1, IP_CAM2, PORT



def conect_cam(IP,PORT):
    import socket
    import json
    from datetime import datetime
    print('ip,port', IP, PORT)
    #HOST, PORT = IP, PORT
    # m ='{"id": 2, "name": "abc"}'
    m = "23" "{\"ACK\":\"\",\"RET\":0}\n\u0003r"  # словарь из лог файла программы DATA MATRIX HONEYWELL
    data = json.dumps(m)
    # Create a socket (SOCK_STREAM means a TCP socket WINDOWS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Содаём подключение....')
    try:
        # Connect to server and send data
        sock.connect((IP, int(PORT)))
        connected = True
        print('Камера подключена')
        sock.sendall(bytes(data, encoding="utf-8"))
        print('Сообщение на камеру отправлено')
        # data_out = {'code_id':'','create_date':''}
        data_out = {}
        while True:
            # Receive data from the server and shut down
            received = sock.recv(1024)
            print('Тип recived', type(received))
            received = received.decode("utf-8")
            received_data = received[:-7]
            print('received_data', received_data)
            # received = received.split('\\')
            time_resiev = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print("Sent:     {}".format(data))
            print("Received: {}".format(received))
            print("Received: {}", received)
            print(time_resiev)
            # print('Тип recived',type(received))
            filename = datetime.now().strftime('%Y-%m-%d')
            print('Код', received[:-7])
            # chek_file()
            if chek_file(received_data) == -1:
                with open(str(filename) + '.json', 'a+') as out_file:
                    # data_out = {}
                    data_scan = {'code_id': received[:-7], 'create_date': time_resiev}
                    data_out.update({'code_id': received[:-7], 'create_date': time_resiev})
                    # print('Тип дата аут', type(data_out))
                    # for line in data_out:
                    # print(type(line))
                    # print('data_out=',data_out)
                    json.dump(data_out, out_file, sort_keys=False, separators=None, ensure_ascii=False)
                    # out_file.write(str(data_out))
                # json.dumps(format(data_out), out_file, indent=6)
                # print(type(out_file))
                # out_file.write('out_data')
                # out_file.write(',')
            # out_file.write(format(received) +'\n')
            # for  line in json.dump(format(received)):
            # file.write(line + '\n')
            # received = sock.recv(1024)
            # received = received.decode("utf-8")
    # finaly:
    except:
        print('Ошибка связи или другая ошибка')
        sock.close()
        print('  Подкючение закрыто, IP,PORT:(',IP,PORT,')')
        IP_r, PORT_r = IP, PORT
        reconect_cam(IP_r,PORT_r)


def reconect_cam(IP_r, PORT_r):
    import time
    connected = False
    time.sleep(10)
    while not connected:
        print('Переподключение, IP,PORT:',IP_r,PORT_r)
        IP = IP_r
        PORT = PORT_r
        conect_cam(IP,PORT)


##Проверяем файл JSON на наличие совпадающих значений ключа code_id
def chek_file(received_data):
    filename = datetime.now().strftime('%Y-%m-%d')
    print('Проверяем файл')
    try:
        with open(str(filename) + '.json', 'r') as fp:
            # data = json.load(fp)
            data = fp.read()
            print('Data=', data)
            print('Тип даты', type(data))
            index = data.find(received_data)
            print('Индекс=', index)
    except:
        index = -1
        print(index)
    finally:
        return index


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


if __name__ == '__main__':
    IP_CAM1 =load_config()[0]
    IP_CAM2 = load_config()[1]
    PORT = load_config()[2]
    print(load_config()[2])
    #IP_CAM1 = load_config[0]
    #IP_CAM2 = IP_Cdef load_config[0]M2
    t1 = Thread(target= conect_cam, args=(IP_CAM1, PORT))
    t2 = Thread(target= conect_cam, args=(IP_CAM2, PORT))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    #conect_cam()
    #reconect_cam()
