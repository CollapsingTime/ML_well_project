import shutil
import json
import os
import itertools
import json
import functools

# Static data from OS and directories for fill info in files
BASE_RESULT_DIR = '/home/vladislav/data/ML_well_project/'
PVT_PATH = '/home/vladislav/data/ML_well_project/_DATA/INCLUDE/PVT'
SCH_PATH = '/home/vladislav/data/ML_well_project/_DATA/INCLUDE/SCH'
STATIC_DATA = {
    "BASE_X": 600,
    "BASE_Y": 500,
    "LAYERS": 80,
    "Z": 0.4,
    "PERM": [0.1, 1, 10, 100, 1000],
    "H": [5, 10, 15, 20, 25],
    "L": [0, 500, 1000, 1500, 2000, 2500],
    "C5_plus": [0, 100, 200, 300, 400],
}
class GenerateInfoForModels:
    """
    Generate info for DATA files
    """
    def __init__(self, static_data: dict = {}, dynamic_data: dict = {}):
        self.st_data = static_data
        self.dyn_data = dynamic_data

    def create_PVT_path(self):
        """
        Find PVT path for new models
        """
        self.st_data['PVT_path'] = {}
        for root, dirs, files in os.walk(PVT_PATH):
            for name in files:
                self.st_data['PVT_path'].setdefault(name, f"{root}/{name}")

    def create_SCH_path(self):
        """
        Find SCH path for new models
        """
        self.st_data['SCH_path'] = {}
        for root, dirs, files in os.walk(SCH_PATH):
            for name in files:
                self.st_data['SCH_path'].setdefault(name, f"{root}/{name}")

    def calculate_NTG(self):
        """
        Calculate NTG for new models
        """
        self.st_data["NTG"] = [round(i/(self.st_data['LAYERS']*self.st_data['Z']), 5) for i in self.st_data['H']]

    def calculate_hectare(self):
        """
        Calculate hectare square
        """
        self.st_data["Hectare"] = [(self.st_data['I'][num] * self.st_data['J'][num] / 100) for num in range(len(self.st_data['L']))]

    def calculate_axes(self):
        """
        Calculate dimensional for new models
        """
        self.st_data['X_axis'] = [(self.st_data['BASE_X']*2+i) for i in self.st_data['L']]
        self.st_data['Y_axis'] = []

        for num in (self.st_data['X_axis']):
            if num == self.st_data['X_axis'][0]:
                self.st_data['Y_axis'].append(int(num/1.7))
            else:
                self.st_data['Y_axis'].append(((int(num/1.7)//100)+1)*100)

        self.st_data['I'] = [int(num/100) for num in self.st_data['X_axis']]
        self.st_data['J'] = [int(num/100) for num in self.st_data['Y_axis']]

    def calculate_volume(self):
        """
        Calculate models volume
        """
        self.st_data['VOLUME'] = []
        for num in range(len(self.st_data['X_axis'])):
            self.st_data['VOLUME'].append(self.st_data['I'][num] * self.st_data['J'][num] * self.st_data['LAYERS'])

    def generate_info(self, methods: dict = dict()):
        """
        Call all functions for fill info about realisations
        """
        for func in dir(self):
            if func.startswith(('calculate', 'create')):
                methods[func] = getattr(self, func)

        for func in methods:
            methods[func]()

    def generate_data_files_info(self):
        """
        Create text file with all realisations data
        """
        item = itertools.count(1)
        for perm, thick, len, c5 in itertools.product(self.st_data['PERM'],
                                                      self.st_data['H'],
                                                      self.st_data['L'],
                                                      self.st_data['C5_plus']):
            # this type of cycles is slower than classic nested cycles
            num = next(item)
            match len:
                case 0:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][0],
                                                   'J': self.st_data['J'][0],
                                                   'Hectare': self.st_data['Hectare'][0],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})
                case 500:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][0],
                                                   'J': self.st_data['J'][0],
                                                   'Hectare': self.st_data['Hectare'][0],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})
                case 1000:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][1],
                                                   'J': self.st_data['J'][1],
                                                   'Hectare': self.st_data['Hectare'][1],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})
                case 1500:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][2],
                                                   'J': self.st_data['J'][2],
                                                   'Hectare': self.st_data['Hectare'][2],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})
                case 2000:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][3],
                                                   'J': self.st_data['J'][3],
                                                   'Hectare': self.st_data['Hectare'][3],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})
                case 2500:
                    self.dyn_data.setdefault(num, {'I': self.st_data['I'][4],
                                                   'J': self.st_data['J'][4],
                                                   'Hectare': self.st_data['Hectare'][4],
                                                   'Well_path': self.st_data["SCH_path"][f"MODEL_SCHEDULE_{len}.inc"],
                                                   'C5+_path': self.st_data["PVT_path"][f"MODEL_PROPS_{c5}.inc"],
                                                   'PERM': perm,
                                                   'H': thick,
                                                   'L': len,
                                                   'C5_plus': c5,
                                                   'NTG': thick/32,})

        with open(f'{BASE_RESULT_DIR}/data_from_realisations.txt', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.dyn_data, indent=4))

    def create_data_files(self):
        """
        Copy default data file and replace information
        """
        for case, params in self.dyn_data.items():
            # print(f"case {case}, params {params}")
            with open('/home/vladislav/data/ML_well_project/_DATA/CASES/test_temp.data', 'r', encoding='utf-8') as file_temp:
                with open(f"/home/vladislav/data/ML_well_project/_TEMP_DATA/{case}_CASE__PERM_{params['PERM']}__Len_{params['L']}__H_{params['H']}__C5_{params['C5_plus']}.data", 'w', encoding='utf-8') as file:
                    for line in file_temp:
                        if '17 10 80 /' in line:
                            file.write(line.replace('17 10 80 /', f"{params['I']} {params['J']} 80 /"))
                        elif '1 17 1 10' in line:
                            file.write(line.replace('1 17 1 10', f"1 {params['I']} 1 {params['J']}"))
                        elif 'NTG=1' in line:
                            file.write(line.replace('NTG=1', f"NTG={params['NTG']}"))
                        elif 'PERMX=0.1' in line:
                            file.write(line.replace('PERMX=0.1', f"PERMX={params['PERM']}"))
                        elif 'INCLUDE/PVT/MODEL_PROPS_0.inc' in line:
                            file.write(line.replace('INCLUDE/PVT/MODEL_PROPS_0.inc', f"{params['C5+_path']}"))
                        elif 'INCLUDE/SCH/MODEL_SCHEDULE_500.inc' in line:
                            file.write(line.replace('INCLUDE/SCH/MODEL_SCHEDULE_500.inc', f"{params['Well_path']}"))
                        else:
                            file.write(line)

test = GenerateInfoForModels(STATIC_DATA)

test.generate_info()
test.generate_data_files_info()
test.create_data_files()