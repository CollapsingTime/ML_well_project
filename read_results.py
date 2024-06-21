import os
import json
import shutil

# Put in your RESULT directory
BASE_RESULT_DIR = '/home/vladislav/Data/Backend/ML_well_project/_DATA/RESULTS_MODEL_DATA'

# Here will be only result file for each path
ONLY_RESULTS = '/home/vladislav/Data/Backend/ML_well_project/_ONLY_RESULTS_FILE'

TOTAL_RESULTS = dict()

class ReadResults:
    def __init__(self, base_path: str, result_path: str, data: dict = {}):
        if isinstance(base_path, str) and isinstance(result_path, str):
            self.base_path = base_path
            self.result_path = result_path
        else:
            raise TypeError('Path must be a str type')
        self.data = data

    @property
    def get_data(self):
        return self.__dict__.items()

    @staticmethod
    def discount_volume(ls: list = None) -> list:
        """
        Create a discount volume from production
        """
        discount = [(1/pow(1+0.14, year)) for year in range(25)]
        return [(ls[i]*discount[i]) for i in range(len(discount))]

    def calc_gas_volume(self, num: int, case: int) -> int:
        """
        Calculate volume of gas with CAPEX and hectare
        """
        dump_datafile = {}
        with open('/home/vladislav/Data/Backend/ML_well_project/data_from_realisations.txt', 'r') as file:
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

        result_dirs = {k: v for k, v in sorted(all_dirs.items(), key=lambda item: item[0])}
        return result_dirs
    
    def create_only_result_dir(self):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        for k, v in self.read_result_path().items():
            if not os.path.exists(f"{self.result_path}/{v}"):
                os.makedirs(f"{self.result_path}/{v}")
            file = f"{self.base_path}/{v}/result.log"
            dir = f"{self.result_path}/{v}/result.log"
            shutil.copy2(file, dir)

    def read_file(self, file_names: list = None) -> list:
        """
        Function can reading all result.log files in all dirs
        """
        file_names = self.read_result_path()
        
        for name in file_names:
            with open(f"{BASE_RESULT_DIR}/{name}/result.log", 'r', encoding='utf-8') as file:
                count = 0
                temp_res = [None for _ in range(25)]
                temp_data = []
                for line in file:
                    if 'TGP=' in line:
                        start = line.find(' TGP=')
                        end = line.find(', TGPH')
                        temp_data.append(float(line[start+5:end]))
                
                for num in range(1, len(temp_data)):
                    temp_data[-num] = (temp_data[-num]-temp_data[-num-1])

                for num in range(1, len(temp_data)-1, 12):
                    temp_res[count] = sum(temp_data[num:num+12])
                    count += 1

                self.data.setdefault(name, {'GAS': self.discount_volume(temp_res)})

    def create_result_file(self, data: dict = dict()) -> dict:
        """
        Create file with total calculated data
        Take all parameters from file name
        """
        for key, value in test.data.items():
                case = [i for i in key.split('_') if i != '' ]
                data.setdefault(case[1], {
                    'Gas': round(self.calc_gas_volume((sum(value['GAS'])), case[1])), 
                    'Years': self.calc_time_working(value['GAS']),
                    'PERM': case[3],
                    'L': case[5],
                    'H': case[7],
                    'C5': case[9],})

        with open('result_file.txt', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=4))

test = ReadResults(BASE_RESULT_DIR, ONLY_RESULTS)

# print(test.read_result_path())
for k, v in test.read_result_path().items():
    print(f"{k} --- {v}")

test.create_only_result_dir()