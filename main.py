from threading import Thread
import time
import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    try:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(os.path.join(os.getcwd()+'/Log/'+log_file))
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        time.sleep(0.1)
        return logger
    except:
        print('Ошибка логера!')


def load_config():
    import configparser
    print('Загружаем конфигурацию оборудования...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        IP_CAM1 = config['CAM1']['IP']
        N_CAM1 = config['CAM1']['N_CAM']
        PORT = config['CAM1']['PORT']
        IP_CAM2 = config['CAM2']['IP']
        N_CAM2 = config['CAM2']['N_CAM']
        IP_CAM3 = config['CAM3']['IP']
        N_CAM3 = config['CAM3']['N_CAM']
        IP_CAM4 = config['CAM4']['IP']
        N_CAM4 = config['CAM4']['N_CAM']
        IP_CAM5 = config['CAM5']['IP']
        N_CAM5 = config['CAM5']['N_CAM']
    except:
        print('Ошибка данных в config.ini')
    return IP_CAM1,N_CAM1, IP_CAM2,N_CAM2,IP_CAM3,N_CAM3,IP_CAM4,N_CAM4,IP_CAM5,N_CAM5, PORT


def conect_cam(IP, PORT, N_CAM):
    import socket
    import json
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + N_CAM
    logger = setup_logger(N_CAM,filename_log+'.log')
    print('ip,port,№CAM', IP, PORT, N_CAM)
    m = "23" "{\"ACK\":\"\",\"RET\":0}\n\u0003r"  # словарь из лог файла программы DATA MATRIX HONEYWELL
    data = json.dumps(m)
    # Create a socket (SOCK_STREAM means a TCP socket WINDOWS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Содаём подключение....')
    logger.info('Подключение к камере '+IP+':'+PORT)
    logger.handlers.clear()
    try:
        # Connect to server and send data
        sock.connect((IP, int(PORT)))
        connected = True
        logger.info('Камера подключена')
        print('Подключена камера', N_CAM)
        sock.sendall(bytes(data, encoding="utf-8"))
        print('Сообщение на камеру отправлено')
        data_out = {}
        while True:
            # Подключаемся к серверу, если соединения нет, перезапускаем подключение
            received = sock.recv(256)
            received = received.decode("utf-8")
            received_data = received[:-7]
            print('received_data', received_data)
            time_resiev = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            print("Sent:     {}".format(data))
            filename = datetime.now().strftime('%Y-%m-%d_')+N_CAM
            logger.info('Код с камеры считан')
            print('Считанный код', received[:-7])
            N_CAM_chk = N_CAM
            logger.handlers.clear()
            if chek_file(received_data, N_CAM_chk) == -1:
                with open(os.path.join(os.getcwd()+'/Code/'+filename) +'.json', 'a+') as out_file:
                    data_scan = {'code_id': received[:-7], 'create_date': time_resiev}
                    data_out.update({'code_id': received[:-7], 'create_date': time_resiev})
                    json.dump(data_out, out_file, sort_keys=False, separators=None, ensure_ascii=False)
                    logger.info('Код записан в JSON файл '+filename +'.json')
                    logger.handlers.clear()
    except:
        print('Ошибка связи или другая ошибка')
        sock.close()
        print('  Подкючение закрыто:',IP+PORT+N_CAM)
        logger.info('Ошибка связи или другая ошибка,Подкючение закрыто')
        logger.handlers.clear()
        IP_r, PORT_r,N_CAM_r = IP, PORT, N_CAM
        reconect_cam(IP_r,PORT_r,N_CAM_r)


def reconect_cam(IP_r, PORT_r,N_CAM_r):
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + N_CAM_r
    logger = setup_logger(N_CAM_r, filename_log + '.log')
    connected = False
    time.sleep(10)
    while not connected:
        logger.info('Переподключение к камере')
        logger.handlers.clear()
        #print('Переподключение, IP,PORT, №Камеры:',IP_r,PORT_r,N_CAM_r)
        IP = IP_r
        PORT = PORT_r
        N_CAM = N_CAM_r
        conect_cam(IP,PORT, N_CAM)


##Проверяем файл JSON на наличие совпадающих значений ключа code_id
def chek_file(received_data,N_CAM):
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + N_CAM
    logger = setup_logger(N_CAM, filename_log + '.log')
    filename = datetime.now().strftime('%Y-%m-%d_')+N_CAM
    print('Проверяем файл', filename, '.json')
    try:
        with open(os.path.join(os.getcwd()+'/Code/'+str(filename)) +'.json', 'r') as fp:
            data = fp.read()
            logger.info('Файл '+filename +'.json'+' готов для записи кодов с камер')
            logger.handlers.clear()
            index = data.find(received_data)
    except:
        index = -1
        print('Файла',filename+N_CAM,'.json не существует')
        print(index)
        logger.info('Файл'++filename +'.json'+' не существует')
        logger.handlers.clear()
    finally:
        return index


if __name__ == '__main__':
    load_config()
    IP_CAM1 =load_config()[0]
    N_CAM1 = load_config()[1]
    IP_CAM2 = load_config()[2]
    N_CAM2 = load_config()[3]
    IP_CAM3 = load_config()[4]
    N_CAM3 = load_config()[5]
    IP_CAM4 = load_config()[6]
    N_CAM4 = load_config()[7]
    IP_CAM5 = load_config()[8]
    N_CAM5 = load_config()[9]
    PORT = load_config()[10]
    if not os.path.exists('Log'):
        os.mkdir('Log')
    if not os.path.exists('Code'):
        os.mkdir('Code')
    t1 = Thread(target= conect_cam, args=(IP_CAM1, PORT, N_CAM1))
    t2 = Thread(target= conect_cam, args=(IP_CAM2, PORT, N_CAM2))
    t3 = Thread(target= conect_cam, args=(IP_CAM3, PORT, N_CAM3))
    t4 = Thread(target= conect_cam, args=(IP_CAM4, PORT, N_CAM4))
    t5 = Thread(target= conect_cam, args=(IP_CAM5, PORT, N_CAM5))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
