import shutil
import json
import os

# Static data from OS and directories for fill info in files
PVT_PATH = '/home/vladislav/data/ML_well_project/_DATA/INCLUDE/PVT'
SCH_PATH = '/home/vladislav/data/ML_well_project/_DATA/INCLUDE/SCH'
STATIC_DATA = {
    "BASE_X": 600,
    "BASE_Y": 500,
    "LAYERS": 80,
    "Z": 0.4,
    "PERM": [0.1, 1, 10, 100, 1000],
    "H": [5, 10, 15, 20, 25],
    "L": [500, 1000, 1500, 2000, 2500],
    "C5_plus": [0, 100, 200, 300, 400],
}
class GenerateInfoForModels:
    """
    Generate info for DATA files
    """
    def __init__(self, data: dict = {}):
        self.data = data

    def create_PVT_path(self):
        """
        Find PVT path for new models
        """
        self.data['PVT_path'] = {}
        for root, dirs, files in os.walk(PVT_PATH):
            for name in files:
                self.data['PVT_path'].setdefault(name, f"{root}/{name}")

    def create_SCH_path(self):
        """
        Find SCH path for new models
        """
        self.data['SCH_path'] = {}
        for root, dirs, files in os.walk(SCH_PATH):
            for name in files:
                self.data['SCH_path'].setdefault(name, f"{root}/{name}")

    def calculate_NTG(self):
        """
        Calculate NTG for new models
        """
        self.data["NTG"] = [round(i/(self.data['LAYERS']*self.data['Z']), 5) for i in self.data['H']]

    def calculate_axes(self):
        """
        Calculate dimensional for new models
        """
        self.data['X_axis'] = [(self.data['BASE_X']*2+i) for i in self.data['L']]
        self.data['Y_axis'] = []

        for num in (self.data['X_axis']):
            if num == self.data['X_axis'][0]:
                self.data['Y_axis'].append(int(num/1.7))
            else:
                self.data['Y_axis'].append(((int(num/1.7)//100)+1)*100)

        self.data['I'] = [int(num/100) for num in self.data['X_axis']]
        self.data['J'] = [int(num/100) for num in self.data['Y_axis']]

    def calculate_volume(self):
        """
        Calculate models volume
        """
        self.data['VOLUME'] = []
        for num in range(len(self.data['X_axis'])):
            self.data['VOLUME'].append(self.data['I'][num] * self.data['J'][num] * self.data['LAYERS'])

    def generate_info(self):
        """
        Calculate and fill all data in object
        """
        methods = {
            "func1": self.create_PVT_path(),
            "func2": self.create_SCH_path(),
            "func3": self.calculate_NTG(),
            "func4": self.calculate_axes(),
            "func5": self.calculate_volume()
        }
        for value in methods.values():
            value

test = GenerateInfoForModels(STATIC_DATA)
test.generate_info()
print(test.data) 




# BASE_DIR = "E:\ml_models\ALL_CASES\\base_case_100.data"

# # All realisations for create new models
# ALL_REALISATIONS = dict()
# count = 1
# for perm in K_PERM:
#     for thick in H:
#         for length in L:
#             for c5 in C5_plus:
#                 match length:
#                     case 500:
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('I', I[0])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('J', J[0])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('Well_path', temp_path_SCH[f"MODEL_SCHEDULE_{length}.inc"])
#                     case 1000:
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('I', I[1])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('J', J[1])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('Well_path', temp_path_SCH[f"MODEL_SCHEDULE_{length}.inc"])
#                     case 1500:
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('I', I[2])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('J', J[2])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('Well_path', temp_path_SCH[f"MODEL_SCHEDULE_{length}.inc"])
#                     case 2000:
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('I', I[3])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('J', J[3])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('Well_path', temp_path_SCH[f"MODEL_SCHEDULE_{length}.inc"])
#                     case 2500:
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('I', I[4])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('J', J[4])
#                         ALL_REALISATIONS.setdefault(count, {}).setdefault('Well_path', temp_path_SCH[f"MODEL_SCHEDULE_{length}.inc"])
#                 ALL_REALISATIONS.setdefault(count, {}).setdefault('PERM', perm)
#                 ALL_REALISATIONS.setdefault(count, {}).setdefault('H', thick)
#                 ALL_REALISATIONS.setdefault(count, {}).setdefault('L', length)
#                 ALL_REALISATIONS.setdefault(count, {}).setdefault('C5+', c5)
#                 ALL_REALISATIONS.setdefault(count, {}).setdefault('NTG', (thick/32))
#                 count += 1

# # add file path with PROPS PVT to ALLREALISATIONS
# for case, value in ALL_REALISATIONS.items():
#     match value['C5+']:
#         case 0:
#             value['C5+_path'] = temp_path_PVT[f"MODEL_PROPS_{value['C5+']}.inc"]
#         case 100:
#             value['C5+_path'] = temp_path_PVT[f"MODEL_PROPS_{value['C5+']}.inc"]
#         case 200:
#             value['C5+_path'] = temp_path_PVT[f"MODEL_PROPS_{value['C5+']}.inc"]
#         case 300:
#             value['C5+_path'] = temp_path_PVT[f"MODEL_PROPS_{value['C5+']}.inc"]
#         case 400:
#             value['C5+_path'] = temp_path_PVT[f"MODEL_PROPS_{value['C5+']}.inc"]

# # Create a file for info from dict
# with open('CREATE_GDM/data_from_realisations.txt', 'w', encoding='utf-8') as file:
#     file.write(json.dumps(ALL_REALISATIONS, indent=4))

# # Create a file copy
# shutil.copy(BASE_DIR, f"E:\ml_models\ALL_CASES\CASES\\test_temp.data")
# shutil.copy(BASE_DIR, f"E:\ml_models\ALL_CASES\CASES\\test.data")

# # Replace all needed info in new file
# with open("E:\ml_models\ALL_CASES\CASES\\test_temp.data", 'r', encoding='utf-8') as file_temp:
#     with open("E:\ml_models\ALL_CASES\CASES\\test.data", 'w', encoding='utf-8') as file:
#         for line in file_temp:
#             if '17 10 80 /' in line:
#                 file.write(line.replace('17 10 80 /', f'{I[4]} {J[4]} 80 /'))
#             elif '1 17 1 10' in line:
#                 file.write(line.replace('1 17 1 10', f'1 {I[4]} 1 {J[4]}'))
#             elif 'NTG=1' in line:
#                 file.write(line.replace('NTG=1', f'NTG={NTG[4]}'))
#             elif 'PERMX=0.1' in line:
#                 file.write(line.replace('PERMX=0.1', f'PERMX={K_PERM[4]}'))
#             else:
#                 file.write(line)

# for case, params in ALL_REALISATIONS.items():
#     temp_dir = case
#     with open("E:\ml_models\ALL_CASES\\base_case_0.data", 'r', encoding='utf-8') as file_temp:
#         with open(f"E:\ml_models\ALL_CASES\\CASE_{temp_dir}__PERM_{params['PERM']}__Len_{params['L']}__H_{params['H']}__C5_{params['C5+']}.data", 'w', encoding='utf-8') as file:
#             for line in file_temp:
#                 if '17 10 80 /' in line:
#                     file.write(line.replace('17 10 80 /', f"{params['I']} {params['J']} 80 /"))
#                 elif '1 17 1 10' in line:
#                     file.write(line.replace('1 17 1 10', f"1 {params['I']} 1 {params['J']}"))
#                 elif 'NTG=1' in line:
#                     file.write(line.replace('NTG=1', f"NTG={params['NTG']}"))
#                 elif 'PERMX=0.1' in line:
#                     file.write(line.replace('PERMX=0.1', f"PERMX={params['PERM']}"))
#                 elif 'INCLUDE/PVT/MODEL_PROPS_0.inc' in line:
#                     file.write(line.replace('INCLUDE/PVT/MODEL_PROPS_0.inc', f"{params['C5+_path']}"))
#                 elif 'INCLUDE/SCH/MODEL_SCHEDULE_500.inc' in line:
#                     file.write(line.replace('INCLUDE/SCH/MODEL_SCHEDULE_500.inc', f"{params['Well_path']}"))
#                 else:
#                     file.write(line)