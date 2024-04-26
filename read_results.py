import shutil
import time
import os

# Put in your RESULT directory
BASE_RESULT_DIR = '/home/vladislav/data/ML_well_project/_DATA/RESULTS'

TOTAL_RESULTS = dict()

class Read_results:
    def __init__(self, path: str, data: dict = {}):
        self.path = path
        self.data = data

    def read_path(self, all_dirs: set = set()) -> list:
        """
        Function pick up and collect all files name in directory
        """
        for root, dirs, files in os.walk(self.path):
            all_dirs.update(dirs)
        return list(all_dirs)
    
    def read_file(self, file_names: list = None) -> list:
        """
        Function can reading all result.log files in all dirs
        """
        file_names = self.read_path()
        
        for name in file_names:
            with open(f"{BASE_RESULT_DIR}/{name}/result.log", 'r', encoding='utf-8') as file:
                temp_data = []
                for line in file:
                    if 'TGP=' in line:
                        start = line.find(' TGP=')
                        end = line.find(', TGPH')
                        temp_data.append(float(line[start+5:end]))
                
                temp_result = []
                for num in range(len(temp_data)-1):
                    temp_result.append(temp_data[num+1]-temp_data[num])

                self.data.setdefault(name, {}).setdefault('GAS', temp_result)


test = Read_results(BASE_RESULT_DIR)
# print(test.read_path())
test.read_file()

print(test.data)

for key, value in test.data.items():
    print(f"{key} === {sum(value['GAS'])}", sep='\n')

# count = 0
# for root, dirs, files in os.walk(BASE_RESULT_DIR):
#     # while count < 7:
#         # You should change / or \ depending on OS
#         with open(f"{BASE_RESULT_DIR}/{dirs[count]}/result.log", 'r', encoding='utf-8') as file:
#             temp = []
#             for line in file:
#                 if 'TGP=' in line:
#                     start = line.find(' TGP=')
#                     end = line.find(', TGPH')
#                     temp_res = line[start+5:end]
#                     temp.append(float(temp_res))
#             temp_res = []
#             for num in range(len(temp)-1):
#                 temp_res.append(temp[num+1]-temp[num])

#             TOTAL_RESULTS.setdefault(dirs[count], {}).setdefault('GAS', temp_res)
#         count += 1

# print(TOTAL_RESULTS)
# print(sum(TOTAL_RESULTS['CASE_254__PERM_10__Len_500__H_5__C5_300']['GAS']))

# res = []

# with open(BASE_DIR, 'r', encoding='utf-8') as file:
#     for line in file:
#         if 'TGP=' in line:
#             start = line.find(' TGP=')
#             end = line.find(', TGPH')
#             temp = line[start+5:end]
#             res.append(float(temp))

# print(res)

# temp = []

# for num in range(len(res)-1):
#     temp.append(res[num+1]-res[num])

# print(sum(temp))

# найти первое вхождение числа в строку, чтобы далее суммировать общее затраченной время
# result_time = []
# with open(BASE_RESULT_DIR, 'r', encoding='utf-8') as file:
#     for line in file:
#         if 'Время расчета' in line:
#             hour, min, sec = line[-10:-2].split('.')
#             print(hour, min, sec)
            # temp = line.find()
            # result_time.append(time.strptime(line[-10:-2], '%H.%M.%S'))

# print(type(result_time[0]))

