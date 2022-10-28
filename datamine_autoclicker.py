import pyautogui as pag
import time
from tqdm import tqdm
import cv2


template = r'F:\Brytkov\Own\PROG\pars\RTS\copy\saver.png'
main_input = r'F:\Brytkov\Own\PROG\pars\RTS\copy\main.png'

phases = [(298, 128), (529, 132), (825, 135), (298, 163), (529, 163), (825, 163)]

def cv(img):
    pag.screenshot('123.png')
    image = cv2.imread(r'F:\Brytkov\Own\PROG\pars\123.png')
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    draft = cv2.imread(img)
    draftGray = cv2.cvtColor(draft, cv2.COLOR_BGR2GRAY)
    
    result = cv2.matchTemplate(imageGray, draftGray, 
	cv2.TM_CCOEFF_NORMED) # компьютерным зрением проверям совпадение по шаблону
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    return {'maxVal': maxVal, 'minVal': minVal}

def clickr(phase):
    time.sleep(.7)
    pag.doubleClick(*phase)
    time.sleep(1.2)
    pag.rightClick(x=701, y=525)#right
    time.sleep(.5)
    pag.click(x=777, y=832)#left (expotr to csv)
    time.sleep(.7)
    pag.click(x=534, y=473)#left (everything)
    time.sleep(.7)
    pag.click(x=791, y=662)#left save
    time.sleep(.5)
    while True:
        res = cv(template)       
        if res['maxVal'] > 0.95: 
            time.sleep(1.2)
            break    
    time.sleep(.3)
    pag.hotkey('enter') # save
    time.sleep(.7)
    pag.click(x=297, y=100)#left back
    time.sleep(.7)

 
pag.click(x=74, y=154) #определение ввода в свойствах
time.sleep(1)
input = cv(main_input)
if input['maxVal'] > 0.98:
	print('\nНайдено, совпадение: ', 100*round(input['maxVal'], 2), '%', '\nЭто основной ввод')
else:
    print('\nНизкая вероятность совпадения: ', 100*round(input['maxVal'], 2), '%', '\nЭто резервный ввод')

time.sleep(.7)
pag.click(x=115, y=213) #left параметры по фазам   
 
[clickr(phase) for phase in tqdm(phases)]










