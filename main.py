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
    except :
        print('Ошибка логера!')


def load_config():
    import configparser
    print('Загружаем конфигурацию оборудования...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        ip_cam1 = config['CAM1']['IP']
        n_cam1 = config['CAM1']['N_CAM']
        port = config['CAM1']['PORT']
        cam1_on = config['CAM1']['CAM_ON']
        ip_cam2 = config['CAM2']['IP']
        n_cam2 = config['CAM2']['N_CAM']
        cam2_on = config['CAM2']['CAM_ON']
        ip_cam3 = config['CAM3']['IP']
        n_cam3 = config['CAM3']['N_CAM']
        cam3_on = config['CAM3']['CAM_ON']
        ip_cam4 = config['CAM4']['IP']
        n_cam4 = config['CAM4']['N_CAM']
        cam4_on = config['CAM4']['CAM_ON']
        ip_cam5 = config['CAM5']['IP']
        n_cam5 = config['CAM5']['N_CAM']
        cam5_on = config['CAM5']['CAM_ON']
        out_setting = [ip_cam1, n_cam1, cam1_on, ip_cam2, n_cam2, cam2_on, ip_cam3, n_cam3, cam3_on,
                       ip_cam4, n_cam4, cam4_on, ip_cam5, n_cam5, cam5_on, port]
        # print('setting1', out_setting[1])
        return out_setting
    except (TypeError,KeyError):
        print('Ошибка данных в config.ini')
        pass


def write_code(received, n_cam):
    from datetime import datetime
    import json
    data_out = {}
    filename = datetime.now().strftime('%Y-%m-%d_') + n_cam
    filename_log = datetime.now().strftime('%Y-%m-%d_') + n_cam
    time_receive = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(os.path.join(os.getcwd() + '/Code/' + filename) + '.json', 'a+') as out_file:
        # data_scan = {'code_id': received[:-7], 'create_date': time_receive}
        data_out.update({'code_id': received, 'create_date': time_receive})
        json.dump(data_out, out_file, sort_keys=False, separators=None, ensure_ascii=False)
        logger = setup_logger(n_cam, filename_log + '.log')
        logger.info('Код записан в JSON файл ' + filename + '.json')
        logger.handlers.clear()
        print('Записан в файл', received)


def connect_cam(ip, port, n_cam):
    import socket
    import json
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + n_cam
    logger = setup_logger(n_cam,filename_log+'.log')
    print('ip,port,№CAM', ip, port, n_cam)
    m = "23" "{\"ACK\":\"\",\"RET\":0}\n\u0003r"  # словарь из лог файла программы DATA MATRIX HONEYWELL
    data = json.dumps(m)
    # Create a socket (SOCK_STREAM means a TCP socket WINDOWS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Содаём подключение....')
    logger.info('Подключение к камере '+ip+':'+port)
    logger.handlers.clear()
    try:
        # Connect to server and send data
        sock.connect((ip, int(port)))
        # connected = True
        logger = setup_logger(n_cam, filename_log + '.log')
        logger.info('Камера подключена '+ip+':'+port)
        logger.handlers.clear()
        print('Подключена камера', n_cam)
        sock.sendall(bytes(data, encoding="utf-8"))
        print('Сообщение на камеру отправлено')
        # data_out = {}
        while True:
            # Подключаемся к серверу, если соединения нет, перезапускаем подключение
            received = sock.recv(1024)
            received = received.decode("utf-8")
            received_data = format(received)
            print('received_data', received_data)
            # time_receive = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            # print("Sent:     {}".format(data))
            # filename = datetime.now().strftime('%Y-%m-%d_')+N_CAM
            logger = setup_logger(n_cam, filename_log + '.log')
            logger.info('Код с камеры считан')
            # print('Считанный код', received[:-7])
            n_cam_chk = n_cam
            logger.handlers.clear()
            for i in range(int(len(received_data)/31)):
                if chek_file(received_data[(0 + i * 31):(24 + i * 31)], n_cam_chk) == -1:
                    write_code(received_data[(0 + i * 31):(24 + i * 31)], n_cam)
            # Если длина полученного сообщения более 70 символов, значит сообщение содержит 3 кода
            # if len(received_data) > 70:
            #     if chek_file(received_data[0:24], n_cam_chk) == -1:
            #         print('received_data[0:24]', received_data[0:24])
            #         write_code(received_data[0:24], n_cam)
            #     if chek_file(received_data[31:55], n_cam_chk) == -1:
            #         print('received_data[31:55]', received_data[31:55])
            #         write_code(received_data[31:55], n_cam)
            #     if chek_file(received_data[62:86], n_cam_chk) == -1:
            #         write_code(received_data[62:86], n_cam)
            # # Если длина полученного сообщения более 70 символов, значит сообщение содержит 2 кода
            # elif len(received_data) > 40:
            #     if chek_file(received_data[0:24], n_cam_chk) == -1:
            #         write_code(received_data[0:24], n_cam)
            #     if chek_file(received_data[31:55], n_cam_chk) == -1:
            #         write_code(received_data[31:55], n_cam)
            # # Если длина полученного сообщения более 70 символов, значит сообщение содержит 1 код
            # else:
            #     if chek_file(received_data[0:24], n_cam_chk) == -1:
            #         write_code(received_data[0:24], n_cam)
    except:
        print('Ошибка связи или другая ошибка')
        sock.close()
        print('  Подкючение закрыто:', ip+port+n_cam)
        logger.info('Ошибка связи или другая ошибка,Подкючение закрыто')
        logger.handlers.clear()
        sock.close()
        ip_r, port_r, n_cam_r = ip, port, n_cam
        reconnect_cam(ip_r, port_r, n_cam_r)


def reconnect_cam(ip_r, port_r, n_cam_r):
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + n_cam_r
    logger = setup_logger(n_cam_r, filename_log + '.log')
    connected = False
    time.sleep(10)
    while not connected:
        logger.info('Переподключение к камере')
        logger.handlers.clear()
        # print('Переподключение, IP,PORT, №Камеры:',ip_r,port_r,n_cam_r)
        ip = ip_r
        port = port_r
        n_cam = n_cam_r
        connect_cam(ip, port, n_cam)


# Проверяем файл JSON на наличие совпадающих значений ключа code_id
def chek_file(received_data, n_cam):
    from datetime import datetime
    filename_log = datetime.now().strftime('%Y-%m-%d_') + n_cam
    logger = setup_logger(n_cam, filename_log + '.log')
    filename = datetime.now().strftime('%Y-%m-%d_') + n_cam
    print('Проверяем файл', filename, '.json')
    try:
        with open(os.path.join(os.getcwd()+'/Code/'+str(filename)) + '.json', 'r') as fp:
            data = fp.read()
            logger.info('Файл '+filename + '.json' + ' готов для записи кодов с камер')
            logger.handlers.clear()
            index = data.find(received_data)
    except:
        index = -1
        print('Файла', filename + n_cam, '.json не существует')
        print(index)
        logger.info('Файл'++filename + '.json' + ' не существует')
        logger.handlers.clear()
    finally:
        return index


if __name__ == '__main__':
    load_config()
    IP_CAM1 = load_config()[0]
    N_CAM1 = load_config()[1]
    cam_1_on = load_config()[2]
    IP_CAM2 = load_config()[3]
    N_CAM2 = load_config()[4]
    cam_2_on = load_config()[5]
    IP_CAM3 = load_config()[6]
    N_CAM3 = load_config()[7]
    cam_3_on = load_config()[8]
    IP_CAM4 = load_config()[9]
    N_CAM4 = load_config()[10]
    cam_4_on = load_config()[11]
    IP_CAM5 = load_config()[12]
    N_CAM5 = load_config()[13]
    cam_5_on = load_config()[14]
    PORT = load_config()[15]
    if not os.path.exists('Log'):
        os.mkdir('Log')
    if not os.path.exists('Code'):
        os.mkdir('Code')
    # Запускаем опрос и обработку каждой камеры в отдельном потоке
    if cam_1_on == 'true':
        t1 = Thread(target=connect_cam, args=(IP_CAM1, PORT, N_CAM1))
        t1.start()
    if cam_2_on == 'true':
        t2 = Thread(target=connect_cam, args=(IP_CAM2, PORT, N_CAM2))
        t2.start()
    if cam_3_on == 'true':
        t3 = Thread(target=connect_cam, args=(IP_CAM3, PORT, N_CAM3))
        t3.start()
    if cam_4_on == 'true':
        t4 = Thread(target=connect_cam, args=(IP_CAM4, PORT, N_CAM4))
        t4.start()
    if cam_5_on == 'true':
        t5 = Thread(target=connect_cam, args=(IP_CAM5, PORT, N_CAM5))
        t5.start()
