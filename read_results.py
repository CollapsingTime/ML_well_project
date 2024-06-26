import os
import json
import shutil

# Put in your RESULT directory
BASE_RESULT_DIR = '/home/vladislav/Data/Backend/ML_well_project/_DATA/RESULTS_MODEL_DATA'

# Here will be only result file for each path
ONLY_RESULTS = '/home/vladislav/Data/Backend/ML_well_project/_ONLY_RESULTS_FILE'

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
        discount = [(1/pow(1+0.14, year)) for year in range(10)]
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
        """
        Function creates a path for only results file
        """
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)

        for k, v in self.read_result_path().items():
            if not os.path.exists(f"{self.result_path}/{v}"):
                os.makedirs(f"{self.result_path}/{v}")
            file = f"{self.base_path}/{v}/result.log"
            dir = f"{self.result_path}/{v}/result.log"
            shutil.copy2(file, dir)

    def read_file(self) -> list:
        """
        Function can reading all result.log files in all dirs
        """
        for _, dir in self.read_result_path().items():
            with open(f"{BASE_RESULT_DIR}/{dir}/result.log", 'r', encoding='utf-8') as file:
                data_file, res_data = [], []
                for line in file:
                    if 'TGP=' in line:
                        data_file.append(float(line[line.find(' TGP=')+5:line.find(', TGPH')]))
                
                for num in range(0, len(data_file)-12, 12):
                    res_data.append(data_file[num+12] - data_file[num])

                self.data.setdefault(dir, {
                    'GAS': self.discount_volume(res_data)})

    def create_result_file(self, data_result: dict = dict()) -> dict:
        """
        Function create file with total calculated data
        Take all parameters from file name
        """
        for key, value in test.data.items():
                case = [i for i in key.split('_') if i != '' ]
                data_result.setdefault(case[0], {
                    'Gas': round(self.calc_gas_volume((sum(value['GAS'])), case[0])), 
                    'Years': self.calc_time_working(value['GAS']),
                    'PERM': case[3],
                    'L': case[5],
                    'H': case[7],
                    'C5': case[9],})

        with open('result_file.txt', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data_result, indent=4))

test = ReadResults(BASE_RESULT_DIR, ONLY_RESULTS)

test.create_only_result_dir()
test.read_file()
test.create_result_file()