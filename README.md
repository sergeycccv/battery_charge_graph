# Battery charge graph
## Анализ логов тестирования батарей ИБП и представление их в графическом виде.

На графиках представлена динамика напряжения, силы тока и мощности на батарее во время тестирования. Вместо времени на оси абсцисс выбран интервал [0; N], где N — количество, например, напряжений в логе.

Обрабатываются все файлы *.txt в текущей директории:

- Если файл один, то откроется окно просмотра графика и сохранится картинка PNG.
- Если два, то их графики будут накладываться друг на друга и сохранится картинка PNG.
Накладывание графиков сделано для наглядного представления двух логов одной батареи, сделанных в разное время. При этом, накладывание графиков может происходить в двух режимах:

    1) без смещения второго графика;
    2) со смещением.
Это сделано из-за возможного разного времени подзарядки батареи. Смещение включается переменной **OFFSET**. Так же нужно учесть, что для корректного наложения необходимо в начале имени файла, в котором записей больше, добавить 1, в котором меньше — 2, чтобы смещался график той батареи, у которой время подзарядки было меньше (сделать это программно лень).

- Если более двух, то изображения графиков сохранятся в виде отдельных PNG без окна просмотра.

Так же на графиках отображается дополнительная информация из лога:

1) Время начала\конца тестирования, подзарядки, разрядки и зарядки. Длительность каждого этапа.
2) Стартовое напряжение.
3) Общая ёмкость и общая мощность батареи на каждом из этапов тестирования.

Пример отдельного графика:

![Один график](example/2022-01-31_09-08.png)

Пример наложенных графиков без смещения:

![Два графика](example/2024-10-02_11-16_2024-10-07_07-38_offset.png)

Пример наложенных графиков со смещением:

![Два графика](example/2024-10-02_11-16_2024-10-07_07-38.png)