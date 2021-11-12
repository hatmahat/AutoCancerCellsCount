"""
Auto Oriented Image Augmentation for Acute Lymphoblastic Leukemia L1
Written by Mahatma Wisesa
"""

import json
import os

# dataset_dir = r"C:\Users\Mahatma Ageng Wisesa\Desktop\Mask RCNN TF2.0\Mask_RCNN\samples\custom"
# annotations = json.load(open(os.path.join(dataset_dir, "train_via_region_data - Copy.json")))

dataset_dir = r"C:\Users\Mahatma Ageng Wisesa\Desktop\Mask RCNN TF2.0\Mask_RCNN\samples\custom"
annotations = json.load(open(os.path.join(dataset_dir, "train_via_project_processed.json")))

keys = annotations.keys() # keys JSON

# IDs contoh output -> [... , 'VH.ALL1.1.1760']
IDs = [ID.split()[0] for ID in keys] # buat IDs dari nomor citra bukan ID JSON

# ORG_IMG contoh output -> [... , 'ALL1.1.1760']
ORG_IMG = [
    ID for ID in IDs if (ID[0] != 'H' and ID[0] != 'V' and ID[:2] != "VH")
    ] # ID untuk citra original yang bukan diaugmentasi

# ORG_JSON_KEYS contoh output -> {... , 'ALL1.1.1760': 'ALL1.1.1760 X B L(BAWAH) (rescaled).jpg146151'}
# ORG_JSON_KEYS -> tujuan = buat ambil regions yg udah dianotasi pada citra asli
ORG_JSON_KEYS = {
    ORG_IMG[i]:list(keys)[i] for i in range(len(ORG_IMG)) if ORG_IMG[i] == list(keys)[i].split()[0]
}

# contoh output {..., VH.ALL1.1.1760': 'VH.ALL1.1.1760 X B L(BAWAH) (rescaled).jpg136287'}
ALL_JSON_KEYS = {
    IDs[i]:list(keys)[i] for i in range(len(IDs))
}
# lanjutan -> ambil augmentasi H ambil IDnya trus ambil org koordinat transofrmasi

IDs_H = [ID[2:] for ID in IDs if ID[:2] == 'H.'] # ID yang ada H-nya
IDs_V = [ID[2:] for ID in IDs if ID[:2] == 'V.']
IDs_VH = [ID[3:] for ID in IDs if ID[:3] == 'VH.']
print(IDs_VH)

# ID = IDs_H[6] # id yg mau diambil listnya
# regions = annotations[ORG_JSON_KEYS[ID]]['regions'] # ambil dict regions

def get_all_points(ID, axis='x'):
    # ambil all_points_x atau all_points_y
    reg_list  = annotations[ORG_JSON_KEYS[ID]]['regions']

    all_points = []
    for reg_dict in reg_list:
        all_points.append(reg_dict['shape_attributes'][f'all_points_{axis}'])
    return all_points

def transformed_points_list(ID, on='H'):
    convert = {
        'H':'x',
        'V':'y'
    }
    # untuk H dulu
    new_points = {}
    n = 0
    for cell in get_all_points(ID, axis=convert[on]):
        n+=1
        new_points[n] = []
        for point in cell:
            # untuk H dulu
            if on == 'H':
                new_points[n].append(820-point)
            elif on == 'V':
                new_points[n].append(614-point)
    n = 0
    # hasil -> points yg udah ter-transform
    return new_points

import copy
def transformed_regions_dict(transformed_list, axis='x'):
    # new_dict = annotations[ORG_JSON_KEYS[ID]]['regions'][0].copy()
    if axis == 'x':
        new_list = annotations[ALL_JSON_KEYS["H."+ID]]['regions']
    elif axis == 'y':
        new_list = annotations[ALL_JSON_KEYS["V."+ID]]['regions']
    elif axis == 'xy':
        new_list = annotations[ALL_JSON_KEYS["VH."+ID]]['regions']
    
    reg_copy = copy.deepcopy(regions)

    n = 0
    for reg_dict in reg_copy:
        n+=1
        if axis == 'x' or axis == 'y':
            reg_dict['shape_attributes'][f'all_points_{axis}'] = transformed_list[n]
        elif axis == 'xy':
            reg_dict['shape_attributes'][f'all_points_x'] = transformed_list[0][n]
            reg_dict['shape_attributes'][f'all_points_y'] = transformed_list[1][n]

        new_list.append(reg_dict)
    n = 0
    return new_list
    
# hapus semua augmentasi
for ID in IDs_H:
    # hapus semua augmentasi
    annotations[ALL_JSON_KEYS["H."+ID]]['regions'].clear()

for ID in IDs_V:
    # hapus semua augmentasi
    annotations[ALL_JSON_KEYS["V."+ID]]['regions'].clear()

for ID in IDs_VH:
    # hapus semua augmentasi
    annotations[ALL_JSON_KEYS["VH."+ID]]['regions'].clear()


for ID in IDs_H:
    regions = annotations[ORG_JSON_KEYS[ID]]['regions']
    transformed_regions_dict(transformed_points_list(ID, 'H'), axis='x')

for ID in IDs_V:
    regions = annotations[ORG_JSON_KEYS[ID]]['regions']
    transformed_regions_dict(transformed_points_list(ID, 'V'), axis='y')

for ID in IDs_VH:
    regions = annotations[ORG_JSON_KEYS[ID]]['regions']
    transformed_regions_dict(
        (transformed_points_list(ID, 'H'), transformed_points_list(ID, 'V')), 
        axis='xy')

# ubah ke file json
with open('new_train_via_region_data.json', 'w') as f:
    json.dump(annotations, f)
print("saved.")