import pandas as pd
import os
from pathlib import Path

phases_name = ['фаза 1', 'фаза 2', 'фаза 3']


def transform(file, t):
    data = pd.read_csv(file, skiprows=range(0, 5),
                       names=['Date and time',
                              f'{t}_Value', f'{t}_Min', f'{t}_Max'],
                       delimiter=';', encoding='utf-8', decimal=",")
    data['Date and time'] = pd.to_datetime(data['Date and time'], errors='coerce', format='%d.%m.%Y %H:%M:%S') 
    data = data.loc[(data['Date and time'] >= '2022-09-01 00:00:00') & (
            data['Date and time'] < '2022-10-26 00:00:00')]  # здесь можно ограничить период

    lst = [1, 2]
    if data.shape[0] % 2 != 0: data = data[:-1]
    [lst.append(i) for _ in range(data.shape[0] // 2 - 1) for i in [1, 2]]
    data['count'] = lst
    return data


def merged(voltage, cur, out):
    data_voltage = transform(voltage, 'U')
    data_cur = transform(cur, "I")

    data = data_voltage.merge(data_cur, on=['Date and time', 'count'], how='left')
    data[['Date and time', 'U_Value', 'U_Min', 'U_Max', 'I_Value', 'I_Min', 'I_Max']].to_csv(out, index=False)


def finder_the_same_phases(directory, phase):
    voltage_meas = [i for i in os.listdir(directory) if f'Напряжение {phase}' in i]
    current_meas = [i for i in os.listdir(directory) if f'Сила тока {phase}' in i]
    merged(Path(directory, *voltage_meas), Path(directory, *current_meas), Path(directory, f'Общее_{phase}.csv'))

