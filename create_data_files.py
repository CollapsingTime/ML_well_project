import json
import os
import shutil
import itertools
import functools
import time
import asyncio
from dotenv import load_dotenv
from random import uniform
from math import log, exp

load_dotenv()

BASE_RESULT_DIR_DATA = os.environ.get('BASE_RESULT_DIR_DATA')
TEST_CASE = os.environ.get('TEST_CASE')
DATA_FILE = os.environ.get('TEMP_DATA')

BASE_PVT_FILE = os.environ.get('BASE_PVT_FILE')
PVT_PATH = os.environ.get('PVT_PATH')

BASE_SCH_FILE = os.environ.get('BASE_SCH_FILE')
BASE_WELLTRACK_FILE = os.environ.get('BASE_WELLTRACK_FILE')
SCH_PATH = os.environ.get('SCH_PATH')

STATIC_DATA = {
    "BASE_X": 600,
    "BASE_Y": 500,
    "LAYERS": 50,
    "Z": 0.4
}

class GenerateInfoForModels:
    """
    Generate info for DATA files
    """
    def __init__(self, static_data: dict = {}):
        self.st_data = static_data

    @staticmethod
    def timer(func: None) -> str:
        """
        Timer for functions
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Time for {func.__name__}: {end-start} seconds")
            return value
        return wrapper
    
    @timer
    def clear_dir(self) -> None:
        ALL_PATHS = [DATA_FILE, PVT_PATH, SCH_PATH]
        ask = input("If 'YES' - all files will be deleted: ")
        for path in ALL_PATHS:
            data_count = {
                'total_file': itertools.count(1),
                'total_dir': itertools.count(1)
            }
            num_file, num_path = 0, 0
            if ask.lower() == 'yes':
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            num_file = next(data_count['total_file'])
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            num_path = next(data_count['total_file'])
                    except Exception as e:
                        print(f'Failed to delete file: {e}')
                print(f"In dir: {path}\nTotal files delete: {num_file}\nTotal paths delete: {num_path}")
            else:
                print('All the files stay in the directory')

    @timer
    def generate_random_static_file(self) -> None:
        """
        Function generates random data for cases
        """
        for case in range(1, 160_001):
            h = uniform(1, 20)
            c5 = uniform(0.1, 400)
            l = uniform(100, 2100)
            perm = exp(1)**uniform(log(0.1), log(100))
            params = {'H': h, 'C5': c5, 'L': l, 'PERM': perm}
            for k, v in params.items():
                self.st_data.setdefault(case, {}).setdefault(k, v)

    @timer
    def update_static_data(self) -> None:
        """
        Function updates static data in class
        """
        for k, v in self.st_data.items():
            self.st_data.setdefault(k, {}).update({'PVT_PATH': f"{PVT_PATH}\\PVTG_{v['C5']}.inc"})
            self.st_data.setdefault(k, {}).update({'SCH_PATH': f"{SCH_PATH}\\MODEL_WELLTRACK_{v['L']}.inc"})
            self.st_data.setdefault(k, {}).update({'NTG': f"{v['H']/STATIC_DATA['LAYERS'] * STATIC_DATA['Z']}"})

            temp_x = int(STATIC_DATA['BASE_X']*2 + v['L'])
            temp_y = int((STATIC_DATA['BASE_X']*2 + v['L'])/1.7)

            self.st_data.setdefault(k, {}).update({'X_axis': f"{temp_x}"})
            self.st_data.setdefault(k, {}).update({'Y_axis': f"{temp_y}"})
            self.st_data.setdefault(k, {}).update({'I': f"{temp_x//100 if temp_x%100 <= 45 else temp_x//100 + 1}"})
            self.st_data.setdefault(k, {}).update({'J': f"{temp_y//100 if temp_y%100 <= 45 else temp_y//100 + 1}"})

            self.st_data.setdefault(k, {}).update({'Hectare': f"{int(self.st_data[k]['I'])*int(self.st_data[k]['J']) / 100}"})

    @timer
    def generate_data(self) -> None:
        """
        Function starts functions which generate files
        """
        for k, v in self.st_data.items():
            self.generate_pvt_file(v['C5'])
            self.generate_sch_file(v['X_axis'], v['Y_axis'], v['L'])

    @staticmethod
    def generate_pvt_file(c5: int) -> None:
        """
        Function generates PVT file for each C5+ value
        """
        with open(BASE_PVT_FILE, 'r') as file:
            with open(f"{PVT_PATH}\\PVTG_{c5}.inc", 'w', encoding='utf-8') as new_file:
                for line in file:
                    temp = line.split()
                    temp_1 = None
                    if len(temp) == 1:
                        new_file.write(str(*temp)+'\n')
                    elif len(temp) == 3 or (len(temp) == 4 and temp[-1] == '/'):
                        temp_1 = ['    '] + ([float(temp[0]) * (c5/150)] + temp[1:] if c5!=0 else temp[1:])
                    elif len(temp) == 4 and temp[-1] == '/':
                        temp_1 = [temp[0]] + ([float(temp[1] * (c5/150))] + temp[2:] if c5!=0 else temp[2:])
                    if temp_1 is not None:
                        new_file.write(" ".join(str(num) for num in temp_1)+'\n')

    @staticmethod
    def generate_sch_file(I: int, J: int, l: int) -> None:
        """
        Function generates welltrack for each well length
        """
        with open(BASE_WELLTRACK_FILE, 'r') as file:
            with open(f"{SCH_PATH}\\MODEL_WELLTRACK_{l}.inc", 'w', encoding='utf-8') as new_file:
                x1 = int(I) - STATIC_DATA['BASE_X']
                y1 = int(J) / 2
                for line in file:
                    temp = line.split()
                    if len(temp) == 4:
                        temp[0], temp[1] = x1, y1
                    elif len(temp) == 5:
                        temp[0], temp[1], temp[3] = x1 - l, y1, 2650 + l
                    new_file.write(" ".join(str(num) for num in temp)+'\n')
    
    async def generate_data_files(self, case, params):
        """

        Copy default data file and replace information

        """
        with open(f"{TEST_CASE}", 'r', encoding='utf-8') as file_temp:
            with open(f"{BASE_RESULT_DIR_DATA}\\DATAFILES\\{case}_CASE__PERM_{int(params['PERM'])}__Len_{int(params['L'])}__H_{int(params['H'])}__C5_{int(params['C5'])}.data", 'w', encoding='utf-8') as file:
                for line in file_temp:
                    if '17 10 50 /' in line:
                        file.write(line.replace('17 10 50 /', f"{params['I']} {params['J']} 50 /"))
                    elif '1 17 1 10' in line:
                        file.write(line.replace('1 17 1 10', f"1 {params['I']} 1 {params['J']}"))
                    elif 'NTG=1' in line:
                        file.write(line.replace('NTG=1', f"NTG={params['NTG']}"))
                    elif 'PERMX=0.1' in line:
                        file.write(line.replace('PERMX=0.1', f"PERMX={params['PERM']}"))
                    elif "'../INCLUDE/PVT/MODELS/PVTG_30.inc' /" in line:
                        file.write(line.replace(f"'../INCLUDE/PVT/MODELS/PVTG_30.inc' /", f"{params['PVT_PATH']}"))
                    elif "'../INCLUDE/SCH/WELLTRACK/MODEL_WELLTRACK_100.inc' /" in line:
                        file.write(line.replace(f"'../INCLUDE/SCH/WELLTRACK/MODEL_WELLTRACK_100.inc' /", f"{params['SCH_PATH']}"))
                    else:
                        file.write(line)

class Calculate:
    def __init__(self):
        self.data = GenerateInfoForModels()

    def clear_data(self):
        self.data.clear_dir()

    def init_data(self):
        self.data.generate_random_static_file()
        self.data.update_static_data()
        self.data.generate_data()

    async def run(self):
        tasks = [asyncio.create_task(self.data.generate_data_files(case, params)) for case, params in self.data.st_data.items()]
        await asyncio.gather(*tasks)
 
result = Calculate()
result.clear_data()
result.init_data()

asyncio.run(result.run())