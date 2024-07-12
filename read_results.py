import os
import json
import shutil
import csv
import time, functools
import asyncio
from dotenv import load_dotenv

load_dotenv()

RESULTS_FROM_MODEL = os.environ.get('RESULTS_FROM_MODEL')
BASE_RESULT_DIR_DATA = os.environ.get('BASE_RESULT_DIR_DATA')
ONLY_RESULTS = os.environ.get('ONLY_RESULTS')

class ReadResults:
    def __init__(self, base_path: str, result_path: str, data: dict = {}, data_result: dict = {}, result_dirs: dict = {}):
        if isinstance(base_path, str) and isinstance(result_path, str):
            self.base_path = base_path
            self.result_path = result_path
        else:
            raise TypeError('Path must be a str type')
        self.data = data
        self.data_result = data_result
        self.result_dirs = result_dirs

    @property
    def get_data(self):
        return self.__dict__.items()

    @staticmethod
    def timer(func: None) -> str:
        """
        Function analysis timer
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            end = time.perf_counter()
            print(f"Time for {func.__name__}: {end-start} seconds")
            return value
        return wrapper

    @staticmethod
    def discount_volume(ls: list = None) -> list:
        """
        Create a discount volume from production
        """
        discount = [(1/pow(1+0.14, year)) for year in range(10)]
        return [(ls[i]*discount[i]) for i in range(len(discount))]

    def calc_gas_volume(self, num: int, case: int) -> int:
        """
        Calculate volume of gas with CAPEX and hectare
        """
        dump_datafile = {}
        with open(f'{BASE_RESULT_DIR_DATA}/data_from_realisations.txt', 'r') as file:
            dump_datafile = json.load(file)
        return num/dump_datafile[case]['Hectare']

    @staticmethod
    def calc_time_working(ls: list = None) -> int:
        """
        Calculate period of working time (in years)
        """
        return len(list(filter(lambda x: x > 0, ls)))

    def read_result_path(self, all_dirs: dict = dict()) -> dict:
        """
        Function picks up, collects and sorts all files name in directory
        """
        for dir in next(os.walk(self.base_path))[1]:
            case = [num for num in dir.split('_') if num != '']
            all_dirs.setdefault(int(case[0]), dir)

        self.result_dirs = {k: v for k, v in sorted(all_dirs.items(), key=lambda item: item[0])}
    
    @timer
    def create_only_result_dir(self) -> None:
        """
        Function creates a path for only results file
        """
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        for k, v in self.result_dirs.items():
            if not os.path.exists(f"{self.result_path}/{v}"):
                os.makedirs(f"{self.result_path}/{v}")
            file = f"{self.base_path}/{v}/result.log"
            dir = f"{self.result_path}/{v}/result.log"
            shutil.copy2(file, dir)

    @timer
    async def read_file(self, dir) -> list:
        """
        Function can reading all result.log files in all dirs
        """
        with open(f"{RESULTS_FROM_MODEL}/{dir}/result.log", 'r', encoding='utf-8') as file:
            data_file, res_data = [], []
            for line in file:
                if 'TGP=' in line:
                    data_file.append(float(line[line.find(' TGP=')+5:line.find(', TGPH')]))
                
            for num in range(0, len(data_file)-12, 12):
                res_data.append(data_file[num+12] - data_file[num])

            self.data.setdefault(dir, {
                'GAS': self.discount_volume(res_data)})

    @timer
    async def create_result_data(self, key, value) -> dict:
        """
        Function create file with total calculated data
        Take all parameters from file name
        """
        case = [i for i in key.split('_') if i != '' ]
        self.data_result.setdefault(case[0], {
                    'Gas': round(self.calc_gas_volume((sum(value['GAS'])), case[0])), 
                    'Years': self.calc_time_working(value['GAS']),
                    'PERM': case[3],
                    'L': case[5],
                    'H': case[7],
                    'C5': case[9],})

    @timer
    def create_result_file(self) -> None:
        """
        Function create file with total calculated data
        Take all parameters from file name
        """
        with open('result_file.csv', 'w', encoding='utf-8', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'Gas', 'Years', 'PERM', 'L', 'H', 'C5'])
            writer.writeheader()
            for key, value in self.data_result.items():
                row = {'id': key}
                row.update(value)
                writer.writerow(row)

class Calculate:
    def __init__(self):
        self.results = ReadResults(RESULTS_FROM_MODEL, ONLY_RESULTS)

    async def run(self):
        self.results.read_result_path()
        self.results.create_only_result_dir()

        tasks_read = [asyncio.create_task(self.results.read_file(dir)) for _, dir in self.results.result_dirs.items()]
        await asyncio.gather(*tasks_read)

        tasks = [asyncio.create_task(self.results.create_result_data(key, value)) for key, value in self.results.data.items()]
        await asyncio.gather(*tasks)

        self.results.create_result_file()

result = Calculate()

asyncio.run(result.run())