import pandas as pd
import csv

phases_name = {'фаза 1': 'Фаза A', 'фаза 2': 'Фаза B', 'фаза 3': 'Фаза C'}


def limiter(df, max_v, min_v, period):
    high = df[(df['U_Max'] > max_v) & (df['Period'] == period) & (df['Power'] == 1)].sort_values(by='U_Max',
                                                                          ascending=False)  # ограничение напряжения и сортировка
    low = df[((df['U_Min'] < min_v) & (df['U_Min'] > 150)) & (df['Period'] == period) & (df['Power'] == 1)].sort_values(by='U_Min', ascending=True)
    high_amount = high.shape[0]  # количество отклонений
    low_amount = low.shape[0]
    dict = {'high': high, 'low': low, 'high_amount': high_amount, 'low_amount': low_amount}
    return dict


def file_writer(meter, name, home, input, obj):
    data = pd.read_csv(meter, skiprows=range(0, 4), names=['Date and time', 'U_Value',
                                                           'U_Min', 'U_Max', 'I_Value', 'I_Min', 'I_Max'],
                       delimiter=',', encoding='utf-8', decimal=".")

    data['Date and time'] = pd.to_datetime(data['Date and time'], errors='coerce')
    data['Power'] = [(1 if (i and i > 0.1) else 0) for i in data["I_Min"]]
    data['Period'] = [('внерабочее время' if i not in range(7, 19) else 'рабочее время')
                      for i in data["Date and time"].dt.hour]  # рабочее/нерабочее время

    work_time = limiter(data, 253, 207, 'рабочее время')
    chill_time = limiter(data, 253, 207, 'внерабочее время')

    with open(f'{name}', 'a+', encoding='utf-8-sig', newline='') as file:
        [file.write(f'\n{input} Ввод {phases_name[i]}\n') for i in phases_name.keys() if i in meter]
        file.write(f'\nВ рабочее время (c 7 до 19):\n')
        file.write(
            f"\nПревышений напряжения: {work_time['high_amount']}\nНизкое напряжение: {work_time['low_amount']}\n")
        file.write(f"\nПревышения напряжения: \n{work_time['high'].head(20)}\n" if work_time['high_amount'] else '')
        file.write(f"\nНизкое напряжение: \n{work_time['low'].head(20)}\n" if work_time['low_amount'] else '')

        file.write(f'\nВо внерабочее время (c 19 до 6):\n')
        file.write(
            f"\nПревышений напряжения: {chill_time['high_amount']}\nНизкое напряжение: {chill_time['low_amount']}\n")
        file.write(f"\nПревышения напряжения: \n{chill_time['high'].head(20)}\n" if chill_time['high_amount'] else '')
        file.write(f"\nНизкое напряжение: \n{chill_time['low'].head(20)}\n" if chill_time['low_amount'] else '')

    with open(f'{home}\\_Результат\\_Итого.csv', 'a+', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow((obj, input, *[f'{phases_name[i]}' for i in phases_name.keys() if i in meter],
                         work_time['high_amount'], work_time['low_amount'], chill_time['high_amount'],
                         chill_time['low_amount']))
