from threading import Thread
import time

def load_config():
    import configparser
    print('Загружаем конфигурацию...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    #print(config['CAM1']['IP'])
    #print(config['CAM1'])
    IP_CAM1 = config['CAM1']['IP']
    N_CAM1 = config['CAM1']['N_CAM']
    #print('ip_cam1',IP_CAM1)
    PORT = config['CAM1']['PORT']
    IP_CAM2 = config['CAM2']['IP']
    N_CAM2 = config['CAM2']['N_CAM']
    return IP_CAM1,N_CAM1, IP_CAM2,N_CAM2, PORT



def conect_cam(IP,PORT,N_CAM):
    import socket
    import json
    from datetime import datetime
    print('ip,port,№CAM', IP, PORT, N_CAM)
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
        data_out = {}
        while True:
            # Подключаемся к серверу, если соединения нет, перезапускаем подключение
            received = sock.recv(256)
            #print('Тип recived', type(received))
            received = received.decode("utf-8")
            received_data = received[:-7]
            print('received_data', received_data)
            time_resiev = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print("Sent:     {}".format(data))
            #print("Received: {}".format(received))
            #print("Received: {}", received)
            #print(time_resiev)
            filename = datetime.now().strftime('%Y-%m-%d_')
            print('Считанный код', received[:-7])
            N_CAM_chk = N_CAM
            #print('N_CAM_chk++++++++++++++',str(filename)+N_CAM_chk,type(N_CAM_chk),type(filename))
            # chek_file()
            if chek_file(received_data, N_CAM_chk) == -1:
                with open(str(filename) + str(N_CAM)+'.json', 'a+') as out_file:
                    data_scan = {'code_id': received[:-7], 'create_date': time_resiev}
                    data_out.update({'code_id': received[:-7], 'create_date': time_resiev})
                    json.dump(data_out, out_file, sort_keys=False, separators=None, ensure_ascii=False)
    except:
        print('Ошибка связи или другая ошибка')
        sock.close()
        print('  Подкючение закрыто, IP,PORT,№CAM:(',IP,PORT,N_CAM,')')
        IP_r, PORT_r,N_CAM_r = IP, PORT, N_CAM
        reconect_cam(IP_r,PORT_r,N_CAM_r)


def reconect_cam(IP_r, PORT_r,N_CAM_r):
    import time
    connected = False
    time.sleep(10)
    while not connected:
        print('Переподключение, IP,PORT, №Камеры:',IP_r,PORT_r,N_CAM_r)
        IP = IP_r
        PORT = PORT_r
        N_CAM = N_CAM_r
        conect_cam(IP,PORT, N_CAM)


##Проверяем файл JSON на наличие совпадающих значений ключа code_id
def chek_file(received_data,N_CAM):
    from datetime import datetime
    filename = datetime.now().strftime('%Y-%m-%d_')
    print('Проверяем файл',filename+N_CAM,'.json')
    try:
        with open(str(filename) + str(N_CAM) +'.json', 'r') as fp:
            data = fp.read()
            index = data.find(received_data)
    except:
        index = -1
        print('Файла',filename+N_CAM,'.json не существует')
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
    load_config()
    IP_CAM1 =load_config()[0]
    N_CAM1 = load_config()[1]
    IP_CAM2 = load_config()[2]
    N_CAM2 = load_config()[3]
    print('CAM2===',N_CAM2)
    PORT = load_config()[4]
    print(load_config()[4])
    t1 = Thread(target= conect_cam, args=(IP_CAM1, PORT,N_CAM1))
    t2 = Thread(target= conect_cam, args=(IP_CAM2, PORT,N_CAM2))

    t1.start()
    t2.start()
    t1.join()
    t2.join()