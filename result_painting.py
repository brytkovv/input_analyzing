from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


cat = Path('F:\Brytkov', 'Работа', '2022', 'Анализ  вводов', 'Объекты', '_Результат')

data = pd.read_csv(f'{cat}\\_Итого.csv', delimiter=';', encoding='utf-8')
 
main_input = data[(data['Ввод'] == 'ОСН')]                   
reserv_input = data[(data['Ввод'] == 'РЕЗ')]    

def painter(input, type_work, type_unw):
    objts = list(set(input['Объект']))
    
    work_time_A = input[type_work][0::3]
    work_time_B = input[type_work][1::3]
    work_time_C = input[type_work][2::3]

    unwork_time_A = input[type_unw][0::3]
    unwork_time_B = input[type_unw][1::3]
    unwork_time_C = input[type_unw][2::3]

    index = np.arange(len(objts))
    bw = 0.3
    cw = 0.27
    
    plt.title('Резервный ввод' if input['Ввод'].head(1).item() == 'РЕЗ' else 'Основной ввод', fontsize=20)

    plt.bar(index, work_time_A, cw, color='b')
    plt.bar(index, unwork_time_A, cw, color ='tab:orange', bottom=work_time_A)
    plt.bar(index+bw, work_time_B, cw, color='b')
    plt.bar(index+bw, unwork_time_B, cw, color ='tab:orange', bottom=work_time_B)
    plt.bar(index+2*bw, work_time_C, cw, color='b')
    plt.bar(index+2*bw, unwork_time_C, cw, color ='tab:orange', bottom=work_time_C)

    plt.xticks(index+bw, sorted(objts), rotation=90)
    
    plt.legend(('Рабочее время (с 7 до 19)', 'Нерабочее время'))
    
    plt.show()
    
# painter(main_input, 'Превышений напряжения в раб. время', 'Превышений напряжения во внераб. время') 
# painter(reserv_input, 'Превышений напряжения в раб. время', 'Превышений напряжения во внераб. время')

# painter(main_input, 'Низкое напряжениев в раб. время', 'Низкое напряжениев во вне раб. время') 
painter(reserv_input, 'Низкое напряжениев в раб. время', 'Низкое напряжениев во вне раб. время')
