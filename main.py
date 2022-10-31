import os
from pathlib import Path
import csv
from logging_resulting import file_writer
from merge import finder_the_same_phases
from tqdm import tqdm

home = Path('F:\Brytkov', 'Own', 'PROG', 'pars', 'RTS', 'project', 'files', 'objects')
# home = Path('C:\environments', 'input_analyzing', 'files', 'objects')
inputs = ['ОСН', 'РЕЗ']
phases_name = ['фаза 1', 'фаза 2', 'фаза 3']

with open(f'{home}\\_Результат\\_Итого.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Объект', 'Ввод', 'Фаза', 'Превышений напряжения в раб. время',
                     'Низкое напряжениев в раб. время', 'Превышений напряжения во внераб. время',
                     'Низкое напряжениев во вне раб. время'])

objs_list = os.listdir(home)[1:]

for objt in tqdm(objs_list):
    for inp in inputs:
        for phase in phases_name:
            directory = f'{home}\\{objt}\\{inp}'
            try:
                finder_the_same_phases(directory, phase)
                [file_writer(f'{directory}\\{meas}', f'{home}\\_Результат\\{objt}.txt', home, inp, objt)
                    for meas in os.listdir(directory) if f'Общее_{phase}' in meas]
            except:
                print(f' Отсутствуют данные по вводу: <{inp} ввод РТС {objt}>')
                

