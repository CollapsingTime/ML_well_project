import shutil
import time
import os


BASE_DIR = 'E:\ml_models\ALL_CASES\RESULTS\\base_case_100\\result.log'

DIR_NAME = 'E:\ml_models\ALL_CASES\RESULTS'

TOTAL_RESULTS = dict()

count = 0
for root, dirs, files in os.walk(DIR_NAME):
    while count < 2:
        with open(f"{DIR_NAME}\\{dirs[count]}\\result.log", 'r', encoding='utf-8') as file:
            temp = []
            for line in file:
                if 'TGP=' in line:
                    start = line.find(' TGP=')
                    end = line.find(', TGPH')
                    temp_res = line[start+5:end]
                    temp.append(float(temp_res))
            temp_res = []
            for num in range(len(temp)-1):
                temp_res.append(temp[num+1]-temp[num])

            TOTAL_RESULTS.setdefault(dirs[count], {}).setdefault('GAS', temp_res)
        count += 1

print(TOTAL_RESULTS)
print(sum(TOTAL_RESULTS['base_case_100']['GAS']))

res = []

# with open(BASE_DIR, 'r', encoding='utf-8') as file:
#     for line in file:
#         if 'TGP=' in line:
#             start = line.find(' TGP=')
#             end = line.find(', TGPH')
#             temp = line[start+5:end]
#             res.append(float(temp))

# print(res)

temp = []

for num in range(len(res)-1):
    temp.append(res[num+1]-res[num])

print(sum(temp))

# найти первое вхождение числа в строку, чтобы далее суммировать общее затраченной время
result_time = []
with open(BASE_DIR, 'r', encoding='utf-8') as file:
    for line in file:
        if 'Время расчета' in line:
            hour, min, sec = line[-10:-2].split('.')
            print(hour, min, sec)
            # temp = line.find()
            # result_time.append(time.strptime(line[-10:-2], '%H.%M.%S'))

# print(type(result_time[0]))

