import os
import json

# Put in your RESULT directory
BASE_RESULT_DIR = '/home/vladislav/data/ML_well_project/_DATA/RESULTS'

TOTAL_RESULTS = dict()

class ReadResults:
    def __init__(self, path: str, data: dict = {}):
        if isinstance(path, str):
            self.path = path
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
        COST_ONE_METER = 0.2

        dump_datafile = {}

        with open('data_from_realisations.txt', 'r') as file:
            dump_datafile = json.load(file)

        return num/dump_datafile[case]['Hectare']

    @staticmethod
    def calc_time_working(ls: list = None) -> int:
        """
        Calculate period of working time
        """
        return len(list(filter(lambda x: x > 0, ls)))

    def read_path(self, all_dirs: set = set()) -> list:
        """
        Function picks up and collects all files name in directory
        """
        for root, dirs, files in os.walk(self.path):
            all_dirs.update(dirs)
        return sorted(all_dirs)
    
    def read_file(self, file_names: list = None) -> list:
        """
        Function can reading all result.log files in all dirs
        """
        file_names = self.read_path()
        
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

    def create_result_file(self):
        """
        Create file with total calculated data
        """
        with open('result_file.txt', 'w', encoding='utf-8') as file:
            for key, value in test.data.items():
                case = [i for i in key.split('_') if i != '' ]
                print(f"{case[1]}={round(self.calc_gas_volume((sum(value['GAS'])), case[1]))}={test.calc_time_working(value['GAS'])}", sep='\n', file=file)

test = ReadResults(BASE_RESULT_DIR)

test.read_file()
test.create_result_file()