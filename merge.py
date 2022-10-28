import pandas as pd


def transform(file, t):
    data = pd.read_csv(file, skiprows=range(0, 4),
                       names=['Date and time',
                              f'{t}_Value', f'{t}_Min', f'{t}_Max'],
                       delimiter=';', encoding='utf-8', decimal=",")

    data['Date and time'] = pd.to_datetime(data['Date and time'])
    lst = [1, 2]
    [lst.append(i) for _ in range(data.shape[0]//2 - 1) for i in [1, 2]]
    data['count'] = lst
    return data


def merged(voltage, cur, out):
    data_voltage = transform(voltage, 'U')
    data_cur = transform(cur, "I")

    data = data_voltage.merge(
        data_cur, on=['Date and time', 'count'], how='left')
    data.to_csv(out)


#merged(r'F:\Brytkov\Own\PROG\pars\RTS\copy\u1.csv', r'F:\Brytkov\Own\PROG\pars\RTS\copy\i1.csv', 'output.csv')
