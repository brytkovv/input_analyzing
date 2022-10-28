import os
from pathlib import Path
import csv
from logging_resulting import file_writer
from tqdm import tqdm

home = Path('F:\Brytkov', 'Работа', '2022', 'Анализ  вводов', 'Объекты')
inputs = ['ОСН', 'РЕЗ']

with open(f'{home}\\_Результат\\_Итого.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Объект', 'Ввод', 'Фаза', 'Превышений напряжения в раб. время', 
                         'Низкое напряжениев в раб. время', 'Превышений напряжения во внераб. время',
                         'Низкое напряжениев во вне раб. время'])

objs_list = os.listdir(home)[2:] 

for objt in tqdm(objs_list):
    for input in inputs:
        dir = f'{home}\\{objt}\\{input}'
        try:
            [file_writer(f'{dir}\\{meter}', f'{home}\\_Результат\\{objt}.txt',
                         home, input, objt)
                  for meter in os.listdir(dir)]
        except:
            print(f' Отсутствуют данные по вводу: <{input} ввод РТС {objt}>')
            