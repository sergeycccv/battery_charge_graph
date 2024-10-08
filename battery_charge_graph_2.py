from datetime import datetime
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def main(FILE_NAME, show_graph=True):

    ROWS_service = []


    # Вход: '2007-12-02 12:30:45:156, выход: '02.12.2007 12:30:45'
    def convert_datetime(str_datetime):
        str_datetime = str_datetime.replace('_', ' ')
        res_dt = datetime.strptime(str_datetime, '%Y.%m.%d %H:%M:%S:%f').strftime('%d.%m.%Y, %H:%M:%S')
        res_dt = datetime.strptime(res_dt, '%d.%m.%Y, %H:%M:%S')
        return res_dt


    # Извлечение C и W
    def get_cw(ROWS_service):
        CW = []
        for i in range(len(ROWS_service)):
            CW.append([])
            for j in range(1, len(ROWS_service[i])):
                ROWS_b = ROWS_service[i][j].split(';')
                buff1 = ROWS_b[2].strip()
                buff2 = ROWS_b[3].strip()
                CW[i].append([float(  buff1[buff1.find('=') + 1:] ), float(  buff2[buff2.find('=') + 1:] )])
        return CW


    def get_data(FILE_NAME):
        I = []
        U = []
        P = []

        ROWS_datetime = []

        with open(FILE_NAME, 'r') as text:
            n = 0
            ns = len(ROWS_service)
            ROWS_service.append([])
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
                    ROWS_service[ns].append(str(n) + ';' + ROWS.strip().replace('+++', ''))

        # Номера аккумулятора из первой строки лога
        n_batt = ROWS_service[ns][0]
        n_batt = n_batt[n_batt.find('№') + 1 : n_batt.find(';', n_batt.find(';') + 1)]

        # Стартовое напряжение из первой строки лога
        U_begin = ROWS_service[ns][0]
        U_begin = U_begin[U_begin.find('=') + 1 : ]

        # Извлечение дат начала и конца тестирования, подзаряда, разряда, заряда и длительности
        datetime_begin_test = convert_datetime(ROWS_datetime[0])
        datetime_end_test = convert_datetime(ROWS_datetime[-1])
        duration_test = datetime_end_test - datetime_begin_test

        datetime_begin_recharge = convert_datetime(ROWS_datetime[0])
        ROWS_b = ROWS_service[ns][1].split(';')
        datetime_end_recharge = convert_datetime(ROWS_datetime[int(ROWS_b[0]) - 1])
        duration_recharge = datetime_end_recharge - datetime_begin_recharge

        datetime_begin_discharge = convert_datetime(ROWS_datetime[int(ROWS_b[0])])
        ROWS_b = ROWS_service[ns][2].split(';')
        datetime_end_discharge = convert_datetime(ROWS_datetime[int(ROWS_b[0]) - 1])
        duration_discharge = datetime_end_discharge - datetime_begin_discharge

        datetime_begin_charge = convert_datetime(ROWS_datetime[int(ROWS_b[0])])
        datetime_end_charge = convert_datetime(ROWS_datetime[-1])
        duration_charge = datetime_end_charge - datetime_begin_charge

        return I, U, P, U_begin, datetime_begin_test, datetime_end_test, datetime_begin_recharge,\
            datetime_end_recharge, datetime_begin_discharge, datetime_end_discharge,\
                datetime_begin_charge, datetime_end_charge, duration_test, duration_recharge,\
                    duration_discharge, duration_charge, n_batt


    '''
    data: list — список значений U, I, P, дат и пр. информации для графиков
    CW: list — список значений C и W для графиков
    FILE_NAME: str — имя файла лога
    fig: plt.figure — общее поле для графиков
    ax1, ax2, ax3: plt.axes — поля для отдельных графиков
    pos_x_y: list — список координат для расположения дополнительных подписей
    '''
    def graph_diff_value(data: list, CW: list, FILE_NAME, fig, ax1, ax2, ax3, pos_x_y: list):
        n = len(data[0])
        ax1.plot(range(n), data[1])
        ax2.plot(range(n), data[0])
        ax3.plot(range(n), data[2])
        ax1.legend(ax1.get_lines(), [i for i in FILE_NAME], loc='lower right')

        if (len(FILE_NAME) == 1) or (len(FILE_NAME) > 2):
            fl = 0
        elif len(FILE_NAME) == 2:
            fl = 1

        text_init = f'{data[16]}:\n' \
                    f'— Файл лога: {FILE_NAME[fl]}\n'\
                    f'— Начало теста: {data[4]}\n'\
                    f'— Конец теста: {data[5]}\n' \
                    f'— Длительность: {data[12]}\n' \
                    f'— U старт: {data[3]}'
        fig.text(pos_x_y[0][0], pos_x_y[0][1], text_init, wrap=True, horizontalalignment='left', fontsize=7)

        text_init = f'Подзаряд:\n' \
                    f'— начало: {data[6]}\n' \
                    f'— конец: {data[7]}\n' \
                    f'— длительность: {data[13]}\n' \
                    f'— C = {CW[0][0]} Ah\n' \
                    f'— W = {CW[0][1]} Wh'
        fig.text(pos_x_y[1][0], pos_x_y[1][1], text_init, wrap=True, horizontalalignment='left', fontsize=7)

        text_init = f'Разряд:\n' \
                    f'— начало: {data[8]}\n' \
                    f'— конец: {data[9]}\n' \
                    f'— длительность: {data[14]}\n' \
                    f'— C = {CW[1][0]} Ah\n' \
                    f'— W = {CW[1][1]} Wh'
        fig.text(pos_x_y[2][0], pos_x_y[2][1], text_init, wrap=True, horizontalalignment='left', fontsize=7)

        text_init = f'Заряд:\n' \
                    f'— начало: {data[10]}\n' \
                    f'— конец: {data[11]}\n' \
                    f'— длительность: {data[15]}\n' \
                    f'— C = {CW[2][0]} Ah\n' \
                    f'— W = {CW[2][1]} Wh'
        fig.text(pos_x_y[3][0], pos_x_y[3][1], text_init, wrap=True, horizontalalignment='left', fontsize=7)

        fig.subplots_adjust(top=pos_x_y[4][0], bottom=pos_x_y[4][1], left=pos_x_y[5][0], right=pos_x_y[5][1])


    # Настройка графиков
    fig = plt.figure(figsize=(11, 9.6))

    # Заголовок окна
    fig = plt.gcf()
    if len(FILE_NAME) == 1:
        title_window = f'Анализ: {FILE_NAME[0]}'
    elif len(FILE_NAME) == 2:
        title_window = f'Анализ: {FILE_NAME[0]} и {FILE_NAME[1]}.'
    else:
        title_window = 'Title'
    fig.canvas.manager.set_window_title(title_window)
    
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

    data = []
    # for i in range(0, len(FILE_NAME)):
    #     data.append( get_data(FILE_NAME[i]) )


    if (len(FILE_NAME) == 1) or (len(FILE_NAME) > 2):

        for i in range(0, len(FILE_NAME)):
            # data.append( get_data(FILE_NAME[i]) )
            # CW = get_cw(ROWS_service)
            

            data = [ get_data(FILE_NAME[i]) ]
            CW = get_cw(ROWS_service)
            fl = [FILE_NAME[i]]
            pos_x_y = [(0.12, 0.92), (0.33, 0.92), (0.52, 0.92), (0.7, 0.92), (0.9, 0.04), (0.07, 0.98)]###################
            graph_diff_value(data[0], CW[0], fl, fig=fig, ax1=ax1, ax2=ax2, ax3=ax3, pos_x_y=pos_x_y)
            # Сохранение результата в png
            file_name_png = FILE_NAME[i].replace('.txt', '') +  '.png'
            fig.savefig(file_name_png, format='png', bbox_inches='tight')

            ax1.remove()
            ax2.remove()
            ax3.remove()
            
            data = []
            CW = []
            if show_graph:
                plt.show()

    elif len(FILE_NAME) == 2:

        for i in range(0, len(FILE_NAME)):
            data.append( get_data(FILE_NAME[i]) )
        CW = get_cw(ROWS_service)

        fl = [FILE_NAME[0]]
        pos_x_y = [(0.01, 0.92), (0.01, 0.84), (0.01, 0.76), (0.01, 0.68), (0.99, 0.01), (0.25, 0.99)]
        graph_diff_value(data[0], CW[0], fl, fig=fig, ax1=ax1, ax2=ax2, ax3=ax3, pos_x_y=pos_x_y)

        fl = [FILE_NAME[0], FILE_NAME[1]]
        pos_x_y = [(0.01, 0.57), (0.01, 0.49), (0.01, 0.41), (0.01, 0.33), (0.99, 0.01), (0.25, 0.99)]
        graph_diff_value(data[1], CW[1], fl, fig=fig, ax1=ax1, ax2=ax2, ax3=ax3, pos_x_y=pos_x_y)

        file_name_png = FILE_NAME[0].replace('.txt', '') + '_' + FILE_NAME[1].replace('.txt', '') + '.png'

    # if len(FILE_NAME) == 1:
    #     file_name_png = FILE_NAME[0].replace('.txt', '') +  '.png'
    # elif len(FILE_NAME) == 2:
    #     file_name_png = FILE_NAME[0].replace('.txt', '') + '_' + FILE_NAME[1].replace('.txt', '') + '.png'
    fig.savefig(file_name_png, format='png', bbox_inches='tight')
    
    if show_graph:
        plt.show()

if __name__ == '__main__':

    # Список текстовых файлов в текущей папке
    FILE_NAME = glob('*.txt')

    if len(FILE_NAME) == 0:
        print('Файлы логов не обнаружены')
        exit()
    elif len(FILE_NAME) == 1:
        main(FILE_NAME)
    elif len(FILE_NAME) == 2:
        main(FILE_NAME)
    else:
        main(FILE_NAME, show_graph=False)
        # file_name_exception = []
        # for i in range(len(FILE_NAME)):
        #     try:
        #         main(FILE_NAME[i], show_graph=False)
        #     except:
        #         print(f'Файл {FILE_NAME[i]} не обработан')
        #         file_name_exception.append(FILE_NAME[i])
        #         continue
        #     print(f'Файл {FILE_NAME[i]} обработан')
        # print('Не удалось обработать следующие файлы: ')
        # for i in range(len(file_name_exception)):
        #     print(f' - {file_name_exception[i]}')
