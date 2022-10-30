import os
from pathlib import Path
import csv
from logging_resulting import file_writer
from merge import finder_the_same_phases
from tqdm import tqdm

# home = Path('F:\Brytkov', 'Работа', '2022', 'Анализ  вводов', 'Объекты')
home = Path('C:\environments', 'input_analyzing', 'files', 'objects')
inputs = ['ОСН', 'РЕЗ']

with open(f'{home}\\_Результат\\_Итого.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Объект', 'Ввод', 'Фаза', 'Превышений напряжения в раб. время',
                     'Низкое напряжениев в раб. время', 'Превышений напряжения во внераб. время',
                     'Низкое напряжениев во вне раб. время'])

objs_list = os.listdir(home)[1:]

# for objt in tqdm(objs_list):
#     for inp in inputs:
#         dire = f'{home}\\{objt}\\{inp}'
#         [finder_the_same_phases(meas, dire) for meas in os.listdir(dire) if 'Напряжение ' in meas]

for objt in tqdm(objs_list):
    for inp in inputs:
        dire = f'{home}\\{objt}\\{inp}'
        [file_writer(f'{dire}\\{meas}', f'{home}\\_Результат\\{objt}.txt', home, inp, objt)
         for meas in os.listdir(dire) if 'Общее_' in meas]

        # except:
        #     print(f' Отсутствуют данные по вводу: <{inp} ввод РТС {objt}>')
