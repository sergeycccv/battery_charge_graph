from datetime import datetime
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import locale


def main(FILE_NAME, show_graph=True):

    I = []
    U = []
    P = []
    ROWS_service = []
    ROWS_datetime = []


# Вход: '2007-12-02 12:30:45:156, выход: '02.12.2007 12:30:45'
    def convert_datetime(str_datetime):
        str_datetime = str_datetime.replace('_', ' ')
        res_dt = datetime.strptime(str_datetime, '%Y.%m.%d %H:%M:%S:%f').strftime('%d.%m.%Y, %H:%M:%S')
        res_dt = datetime.strptime(res_dt, '%d.%m.%Y, %H:%M:%S')
        return res_dt


    # Извлечение C и W
    def get_cw(column):
        ROWS_b = ROWS_service[column].split(';')
        buff = ROWS_b[2].strip()
        C = float(  buff[buff.find('=') + 1:] )
        buff = ROWS_b[3].strip()
        W = float(  buff[buff.find('=') + 1:] )
        return C, W


    def get_data(FILE_NAME):
        with open(FILE_NAME, 'r') as text:
            n = 0
            for ROWS in text:
                if ROWS[0] != '+':
                    if ROWS != '\n':
                        ROWS = ROWS.replace(' ', '').strip()
                        ROWS = ROWS[:-1]
                        ROWS = ROWS.split(';')
                        I.append(float(ROWS[1]))
                        U.append(float(ROWS[2]))
                        P.append(float(ROWS[3]))
                        ROWS_datetime.append(ROWS[0])
                        n += 1
                else:
                    # Запоминаем строку, хранящую дату/время начала подзаряда, заряда, разряда
                    ROWS_service.append(str(n) + ';' + ROWS.strip().replace('+++', ''))

        # Номера аккумулятора из первой строки лога
        n_batt = ROWS_service[0]
        n_batt = n_batt[n_batt.find('№') + 1 : n_batt.find(';', n_batt.find(';') + 1)]

        # Стартовое напряжение из первой строки лога
        U_begin = ROWS_service[0]
        U_begin = U_begin[U_begin.find('=') + 1 : ]

        # Извлечение дат начала и конца тестирования, подзаряда, разряда, заряда и длительности
        datetime_begin_test = convert_datetime(ROWS_datetime[0])
        datetime_end_test = convert_datetime(ROWS_datetime[-1])
        duration_test = datetime_end_test - datetime_begin_test

        datetime_begin_recharge = convert_datetime(ROWS_datetime[0])
        ROWS_b = ROWS_service[1].split(';')
        datetime_end_recharge = convert_datetime(ROWS_datetime[int(ROWS_b[0]) - 1])
        duration_recharge = datetime_end_recharge - datetime_begin_recharge

        datetime_begin_discharge = convert_datetime(ROWS_datetime[int(ROWS_b[0])])
        ROWS_b = ROWS_service[2].split(';')
        datetime_end_discharge = convert_datetime(ROWS_datetime[int(ROWS_b[0]) - 1])
        duration_discharge = datetime_end_discharge - datetime_begin_discharge

        datetime_begin_charge = convert_datetime(ROWS_datetime[int(ROWS_b[0])])
        datetime_end_charge = convert_datetime(ROWS_datetime[-1])
        duration_charge = datetime_end_charge - datetime_begin_charge


        return I, U, P, U_begin, datetime_begin_test, datetime_end_test, datetime_begin_recharge,\
            datetime_end_recharge, datetime_begin_discharge, datetime_end_discharge,\
                datetime_begin_charge, datetime_end_charge, duration_test, duration_recharge,\
                    duration_discharge, duration_charge, n_batt

    
    I, U, P, U_begin, datetime_begin_test, datetime_end_test, datetime_begin_recharge,\
            datetime_end_recharge, datetime_begin_discharge, datetime_end_discharge,\
                datetime_begin_charge, datetime_end_charge, duration_test, duration_recharge,\
                    duration_discharge, duration_charge, n_batt = get_data(FILE_NAME)


    fig = plt.figure(figsize=(11, 9.6))

    # Заголовок окна
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(f'Анализ: {FILE_NAME}')

    # plt.suptitle(f'Тест: {n_batt} | Файл лога: {FILE_NAME}', size=11, fontweight='bold', y=0.94)

    gs = GridSpec(ncols=2, nrows=3, figure=fig)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_ylabel('U, V')
    ax1.grid()

    ax2 = fig.add_subplot(gs[1, :])
    ax2.set_ylabel('I, A')
    ax2.grid()

    ax3 = fig.add_subplot(gs[2, :])
    ax3.set_ylabel('P, W')
    ax3.grid()


    ax1.plot(range(len(U)), U)
    # ax1.set_title(f'Стартовое напряжение: {U_begin} V', x=0.2, size=10)
    ax2.plot(range(len(I)), I)
    ax3.plot(range(len(P)), P)
    ax1.legend(ax1.get_lines(), [FILE_NAME, '60000 V'], loc='lower right')

    
    text_init = f'{n_batt}:\n' \
                f'— Файл лога: {FILE_NAME}\n'\
                f'— Начало теста: {datetime_begin_test}\n'\
                f'— Конец теста: {datetime_end_test}\n' \
                f'— Длительность: {duration_test}\n' \
                f'— U старт: {U_begin}'
    plt.figtext(0.12, 0.92, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Подзаряд:\n' \
                f'— начало: {datetime_begin_recharge}\n' \
                f'— конец: {datetime_end_recharge}\n' \
                f'— длительность: {duration_recharge}\n' \
                f'— C = {get_cw(1)[0]} Ah\n' \
                f'— W = {get_cw(1)[1]} Wh'
    plt.figtext(0.33, 0.92, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Разряд:\n' \
                f'— начало: {datetime_begin_discharge}\n' \
                f'— конец: {datetime_end_discharge}\n' \
                f'— длительность: {duration_discharge}\n' \
                f'— C = {get_cw(2)[0]} Ah\n' \
                f'— W = {get_cw(2)[1]} Wh'
    plt.figtext(0.52, 0.92, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Заряд:\n' \
                f'— начало: {datetime_begin_charge}\n' \
                f'— конец: {datetime_end_charge}\n' \
                f'— длительность: {duration_charge}\n' \
                f'— C = {get_cw(3)[0]} Ah\n' \
                f'— W = {get_cw(3)[1]} Wh'
    plt.figtext(0.7, 0.92, text_init, wrap=True, horizontalalignment='left', fontsize=7)


    fig.subplots_adjust(top=0.9, bottom=0.04, left=0.07, right=0.98)

    plt.savefig(FILE_NAME[:-4] + '.png', format='png', bbox_inches='tight')
    
    if show_graph:
        plt.show()

if __name__ == '__main__':

    locale.setlocale(category=locale.LC_ALL, locale='ru_RU.UTF-8')

    # Список текстовых файлов в текущей папке
    FILE_NAME = glob('*.txt')

    if len(FILE_NAME) == 0:
        print('Файлы логов не обнаружены')
        exit()
    elif len(FILE_NAME) == 1:
        main(FILE_NAME[0])
    elif len(FILE_NAME) == 2:
        main(FILE_NAME[0])
        main(FILE_NAME[1])
    else:
        file_name_exception = []
        for i in range(len(FILE_NAME)):
            try:
                main(FILE_NAME[i], show_graph=False)
            except:
                print(f'Файл {FILE_NAME[i]} не обработан')
                file_name_exception.append(FILE_NAME[i])
                continue
            print(f'Файл {FILE_NAME[i]} обработан')
        print('Не удалось обработать следующие файлы: ')
        for i in range(len(file_name_exception)):
            print(f' - {file_name_exception[i]}')
