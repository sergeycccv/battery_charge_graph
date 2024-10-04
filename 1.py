    text_init = f'{n_batt}:\n' \
                f'— Файл лога: {FILE_NAME}\n'\
                f'— Начало теста: {datetime_begin_test}\n'\
                f'— Конец теста: {datetime_end_test}\n' \
                f'— Длительность: {duration_test}\n' \
                f'— U старт: {U_begin}'
    plt.figtext(0.01, 0.92, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Подзаряд:\n' \
                f'— начало: {datetime_begin_recharge}\n' \
                f'— конец: {datetime_end_recharge}\n' \
                f'— длительность: {duration_recharge}\n' \
                f'— C = {get_cw(1)[0]} Ah\n' \
                f'— W = {get_cw(1)[1]} Wh'
    plt.figtext(0.01, 0.84, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Разряд:\n' \
                f'— начало: {datetime_begin_discharge}\n' \
                f'— конец: {datetime_end_discharge}\n' \
                f'— длительность: {duration_discharge}\n' \
                f'— C = {get_cw(2)[0]} Ah\n' \
                f'— W = {get_cw(2)[1]} Wh'
    plt.figtext(0.01, 0.76, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    text_init = f'Заряд:\n' \
                f'— начало: {datetime_begin_charge}\n' \
                f'— конец: {datetime_end_charge}\n' \
                f'— длительность: {duration_charge}\n' \
                f'— C = {get_cw(3)[0]} Ah\n' \
                f'— W = {get_cw(3)[1]} Wh'
    plt.figtext(0.01, 0.68, text_init, wrap=True, horizontalalignment='left', fontsize=7)

    fig.subplots_adjust(top=0.99, bottom=0.17, left=0.25, right=0.99)
