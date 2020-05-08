# Importing Libraries
import math
from shapely.geometry import Polygon
import numpy as np
import os,io
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson
import re


row_col_dict = {(0, 0): {'actual': 'missing', 'expected': 'dark_fantasy', 'coordinates': None, 'confidence': None}, (0, 3): {'actual': 'missing', 'expected': 'boil_in_bag_brown_rice', 'coordinates': None, 'confidence': None}, (0, 1): {'actual': 'natures_promise_honey', 'expected': 'natures_promise_honey', 'coordinates': [337, 96, 506, 302], 'confidence': 76}, (0, 2): {'actual': 'boil_in_bag_white_rice', 'expected': 'boil_in_bag_white_rice', 'coordinates': [538, 156, 665, 319], 'confidence': 80}, (1, 0): {'actual': 'rigatony', 'expected': 'rigatony', 'coordinates': [227, 471, 334, 602], 'confidence': 74}, (1, 1): {'actual': 'farfalle', 'expected': 'farfalle', 'coordinates': [378, 488, 485, 605], 'confidence': 92}, (1, 2): {'actual': 'kitkat', 'expected': 'kitkat', 'coordinates': [529, 522, 673, 614], 'confidence': 87}, (1, 3): {'actual': 'ziti', 'expected': 'ziti', 'coordinates': [729, 485, 837, 598], 'confidence': 98}, (2, 0): {'actual': 'missing', 'expected': 'puffed_wheat', 'coordinates': None, 'confidence': None}, (2, 1): {'actual': 'boil_in_bag_brown_rice', 'expected': 'boil_in_bag_brown_rice', 'coordinates': [408, 754, 510, 882], 'confidence': 78}, (2, 2): {'actual': 'oats_and_os', 'expected': 'oats_and_os', 'coordinates': [531, 700, 698, 872], 'confidence': 97}, (2, 3): {'actual': 'puffed_rice', 'expected': 'puffed_rice', 'coordinates': [702, 690, 872, 879], 'confidence': 97}, (3, 0): {'actual': 'missing', 'expected': 'oats_and_os', 'coordinates': None, 'confidence': None}, (3, 3): {'actual': 'puffed_rice', 'expected': 'frosted_shredded_wheat', 'coordinates': [683, 974, 849, 1159], 'confidence': 87}, (3, 1): {'actual': 'natures_promise_raisin', 'expected': 'natures_promise_raisin', 'coordinates': [371, 975, 513, 1137], 'confidence': 80}, (3, 2): {'actual': 'frosted_shredded_wheat', 'expected': 'frosted_shredded_wheat', 'coordinates': [529, 976, 674, 1151], 'confidence': 92}, (4, 0): {'actual': 'missing', 'expected': 'chocos_500g', 'coordinates': None, 'confidence': None}, (4, 3): {'actual': 'ziti', 'expected': 'boil_in_bag_brown_rice', 'coordinates': [728, 1277, 824, 1392], 'confidence': 72}, (4, 1): {'actual': 'boil_in_bag_white_rice', 'expected': 'boil_in_bag_white_rice', 'coordinates': [380, 1264, 486, 1393], 'confidence': 97}, (4, 2): {'actual': 'boil_in_bag_brown_rice', 'expected': 'boil_in_bag_brown_rice', 'coordinates': [568, 1262, 666, 1386], 'confidence': 97}} 


def convert_dict(row_col_dict):
    final = {}
    for key in row_col_dict.keys():
        temp_dict = row_col_dict[key]
        if temp_dict['coordinates'] == None:
            continue
        else:
            temp_key = temp_dict['actual']
            l = temp_dict['coordinates']
            coods = [l[0], l[1], l[0], l[3], l[2], l[3], l[2], l[1]]
            if temp_key in final.keys():
                final[temp_key].append(coods)
            else:
                final[temp_key] = [coods]
                
    return final

detected_obj = convert_dict(row_col_dict)


def row_col_cood(row_col_dict):
    dict_row = {}
    for key in row_col_dict.keys():
        temp_dict = row_col_dict[key]
        dict_row[key] = temp_dict['coordinates']
        
    return dict_row

checking_dict = row_col_cood(row_col_dict)

# Image Location
file_name='test4.jpg'
folder_path=r'C:\Ahold'


# Get all Text Coordinates from GCP
def google_text_detection(file_name, folder_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'unified-skein-267807-7e4a724af631.json'
    client=vision.ImageAnnotatorClient()
    
    with io.open(os.path.join(folder_path,file_name),'rb') as image_file:
        content = image_file.read()
            
    image=vision.types.Image(content=content)
    response=client.text_detection(image=image)
    
    texts = response.text_annotations
    
    for text in texts:
        x=re.findall("(?:[\$]{1}[,\d]+.?\d*)", text.description)
        break
    
    dict_detect_price = {}
        
    dict_detect_text = {}
    count = 0
    
    for text in texts:
        if count == 0:
            count += 1
            continue
        text_des = '{}'.format(text.description)
        vertices = ([(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])
        flag = True
        
        for key in x:
            if key in text_des:
                flag = False
                if key in dict_detect_price.keys():
                    dict_detect_price[key].append(vertices)
                else:
                    dict_detect_price[key] = [vertices]
                    
        if flag:
            if text_des in dict_detect_text.keys():
                dict_detect_text[text_des].append(vertices)
            else:
                dict_detect_text[text_des] = [vertices]
            
    
                    
    return dict_detect_text, dict_detect_price


dict_all_text_cood, text_cood = google_text_detection(file_name, folder_path)
    
  
actual_obj_length = {
    'rack': 8,
    'natures_promise_honey': 12,
    'natures_promise_raisin': 12,
    'oats_and_os': 12,
    'puffed_rice': 12,
    'puffed_wheat': 12,
    'frosted_shredded_wheat': 12,
    'chocos_125g': 9,
    'boil_in_bag_white_rice' : 9,
    'boil_in_bag_brown_rice' : 9,
    'rigatony': 9,
    'farfalle': 9,
    'kitkat': 4,
    'ziti': 9
}

def productName():
    productDetails = {
        
            "boil_in_bag_brown_rice": {
                "product_name": "Boil In Bag Brown Rice"

            },

            "boil_in_bag_white_rice": {
                "product_name": "Boil In Bag White Rice"

            },

            "chocos_500g": {
                "product_name": "Chocos 500g"

            },

            "dark_fantasy": {
                "product_name": "Dark Fantasy"

            },

            "farfalle": {
                "product_name": "FarFalle"

            },

            "frosted_shredded_wheat": {
                "product_name": "Frosted Shredded Wheat"

            },

            "kitkat": {
                "product_name": "kitkat"

            },

            "natures_promise_honey": {
                "product_name": "Natures Promise Honey"

            },

            "natures_promise_raisin": {
                "product_name": "Natures Promise Raisin Bran"

            },

            "oats_and_os": {
                "product_name": "Oats and Os"

            },

            "puffed_rice": {
                "product_name": "Puffed Rice"

            },
            "puffed_wheat": {
                "product_name": "Puffed Wheat"

            },
            "rigatony": {
                "product_name": "Rigatoni"

            },
            "ziti": {
                "product_name": "Ziti"

            }

            
    }
    return (productDetails)

product_details = productName()


rack = actual_obj_length['rack']
del actual_obj_length['rack']


# Euclidian Distance
def distance_cood(list_of_coods):
    p1 = (list_of_coods[0], list_of_coods[2])
    p2 = (list_of_coods[1], list_of_coods[3])
    height = math.sqrt(((abs(p1[0] - p1[1]))**2) + ((abs(p2[0] - p2[1]))**2))
    
    return height


# Calculate height of the products from detected objects
def calc_length(detected_obj):
    dict_lengths = {}
    for key in detected_obj.keys():
        length_of_all = []
        l = detected_obj[key]
        for i in range(len(l)):
            list_of_coods_left = l[i][0:4]
            list_of_coods_right = l[i][4:8]
            length = [distance_cood(list_of_coods_left), distance_cood(list_of_coods_right)]
            length_of_all.append(length)
        dict_lengths[key] = length_of_all
    return dict_lengths




detected_obj_length = calc_length(detected_obj)


# Calculate the ratio for each product
def ratios(detected_obj_length, actual_obj_length):
    dict_ratios = {}
    for key in detected_obj_length.keys():
        ratio_of_all = []
        l = detected_obj_length[key]
        for i in range(len(l)):
            ratio1 = l[i][0]/actual_obj_length[key]
            ratio2 = l[i][1]/actual_obj_length[key]
            ratios = [ratio1, ratio2]
            ratio_of_all.append(ratios)
        dict_ratios[key] = ratio_of_all
    return dict_ratios



detected_obj_ratios = ratios(detected_obj_length, actual_obj_length)


# Getting the median of all the ratios
def calc_median(detected_obj_ratios):
    l_left = []
    l_right = []
    for key in detected_obj_ratios:
        l = detected_obj_ratios[key]
        for i in range(len(l)):
            l_left.append(l[i][0])
            l_right.append(l[i][1])
    sorted(l_left)
    sorted(l_right)
    return [l_left[len(l_left)//2], l_right[len(l_right)//2]]


median = calc_median(detected_obj_ratios)


rack = [rack*median[0], rack*median[1]]


# Calculating Respective Rack Coordinates of the products
def rack_cood(detected_obj, rack):
    dict_rack = {}
    for key in detected_obj.keys():
        cood_of_rack = []
        l = detected_obj[key]
        for i in range(len(l)):
            cood_of_single_rack = [[max(l[i][0], l[i][2]), l[i][3]], [max(l[i][0], l[i][2]), (l[i][3] + rack[0])], [max(l[i][4], l[i][6]), (l[i][5] + rack[1])], [max(l[i][4], l[i][6]), l[i][5]]]
            
            cood_of_rack.append(cood_of_single_rack)
        dict_rack[key] = cood_of_rack
    return dict_rack



res_cood = rack_cood(detected_obj, rack)


# Euclidian Distance and returning 10% of length
def distance_length_cood(list_of_coods):
    p1 = (list_of_coods[0][0], list_of_coods[3][0])
    p2 = (list_of_coods[0][1], list_of_coods[3][1])
    length = math.sqrt(((abs(p1[0] - p1[1]))**2) + ((abs(p2[0] - p2[1]))**2))
    
    length = 0.1*length
    
    return length

# Increasing the rack coordinates by extra 10% of their length 
res_cood_1 = rack_cood(detected_obj, rack)
for key in res_cood.keys():
    l = res_cood_1[key]
    for i in range(len(l)):
        length = distance_length_cood(l[i])
        l[i] = [[l[i][0][0] - length, l[i][0][1]], [l[i][1][0] - length, l[i][1][1]], [l[i][2][0] + length, l[i][2][1]], [l[i][3][0] + length, l[i][3][1]]]
        


# Calculating intersection area
def calculate_intersection(box_1, box_2):
    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)
    intersection_area = poly_1.intersection(poly_2).area
    return intersection_area


# Euclidian Distance and returning n% of length
def distance_length_rack_cood(list_of_coods, n):
    p1 = (list_of_coods[0][0], list_of_coods[3][0])
    p2 = (list_of_coods[0][1], list_of_coods[3][1])
    length = math.sqrt(((abs(p1[0] - p1[1]))**2) + ((abs(p2[0] - p2[1]))**2))  
    length = n*length  
    return length

# Decreasing the length of rack by n%
def set_cood(l, n):
    length = distance_length_rack_cood(l, n)
    l = [[l[0][0] + length, l[0][1]], [l[1][0] + length, l[1][1]], [l[2][0] - length, l[2][1]], [l[3][0] - length, l[3][1]]]
    return l

# Checking overlap of the rack and text area and decreasing the length until intersection area is zero
def check_overlap_rack(res_cood):
    rack_list = []
    l_of_rack = []
    l_of_rack_cood = []
    final_dict = {}

    for key in res_cood.keys():
        l = res_cood[key]
        for i in range(len(l)):
            l_of_rack.append(key)
            l_of_rack_cood.append(l[i])
            
    for i in range(len(l_of_rack_cood)):
        final_list = []
        box1 = l_of_rack_cood[i]
        n = 0.01
        for j in range(len(l_of_rack_cood)):
            if (i == j):
                continue
            box2 = l_of_rack_cood[j]
            area = calculate_intersection(box1, box2)
            if area != 0:
                j -= 1
                l_of_rack_cood[i] = set_cood(l_of_rack_cood[i], n)
                l_of_rack_cood[j] = set_cood(l_of_rack_cood[j], n)
                n += 0.01
                continue
            final_list.append(calculate_intersection(box1, box2))
            
        rack_list.append(final_list)
        
    
    for i in range(len(l_of_rack)):
        if l_of_rack[i] in final_dict.keys():
            list_change = final_dict[l_of_rack[i]]
            list_change.append(l_of_rack_cood[i])
        else:
            final_dict[l_of_rack[i]] = [l_of_rack_cood[i]]

    return final_dict




res_cood = check_overlap_rack(res_cood_1)

# Checking intersection area of price and rack
def check_overlap(text_cood_four, res_cood):
    dict_area = {}
    for rack_key in res_cood.keys():
        area_of_text = []
        l_rack = res_cood[rack_key]
        for i in range(len(l_rack)):
            l = []
            box_1 = l_rack[i]
            for text_key in text_cood_four.keys():
                l_text = text_cood_four[text_key]
                for i in range(len(l_text)):
                    box_2 = l_text[i]
                    area_overlap = calculate_intersection(box_1, box_2)
                    l.append(area_overlap)
            area_of_text.append(l)
        dict_area[rack_key] = area_of_text
    return dict_area


dict_res = check_overlap(text_cood, res_cood)


# Calculating area of a rectangle
def area_text(list_text_cood):
    poly_text = Polygon(list_text_cood)
    area = poly_text.area
    return area


# Getting Product Prices and storing it in a dictionary with their respective ratio of intersection
def price_matching(dict_res, text_cood):
    dict_price = {}
    l_of_text = []
    l_of_text_cood = []

    for key in text_cood.keys():
        l = text_cood[key]
        for i in range(len(l)):
            l_of_text.append(key)
            l_of_text_cood.append(l[i])
    
    for key in dict_res.keys():
        l_check = []
        l = dict_res[key]
        for i in range(len(l)):
            if (max(l[i]) == 0):
                l_check.append('Price is Missing')
                dict_price[key] = l_check
                continue
            else:
                for j in range(len(l[i])):
                    if l[i][j] == 0:
                        continue
                    else:
                        l_check.append([l_of_text[j], (l[i][j]/area_text(l_of_text_cood[j]))])
                dict_price[key] = l_check
    return dict_price



dict_price = price_matching(dict_res, text_cood)
    
    
dict_results = check_overlap(dict_all_text_cood, res_cood)


# Getting all the text in product rack coordinates
def final_price_matching(dict_res, text_cood):
    dict_price = {}
    l_of_text = []
    l_of_text_cood = []

    for key in text_cood.keys():
        l = text_cood[key]
        for i in range(len(l)):
            l_of_text.append(key)
            l_of_text_cood.append(l[i])
    
    for key in dict_res.keys():
        l_check = []
        l = dict_res[key]
        for i in range(len(l)):
            if (max(l[i]) == 0):
                l_check.append('No Text')
                dict_price[key] = l_check
                continue
            else:
                final_list = []
                for j in range(len(l[i])):
                    if l[i][j] == 0:
                        continue
                    else:
                        if l[i][j]/area_text(l_of_text_cood[j]) < 0.5:
                            continue
                        final_list.append(l_of_text[j])
                l_check.append(final_list)
                dict_price[key] = l_check
    return dict_price




final_dict = final_price_matching(dict_results, dict_all_text_cood)

def Punctuation(string): 
  
    # punctuation marks 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~ '''
  
    # traverse the given string and if any punctuation 
    # marks occur replace it with null 
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
  
    # Print string without punctuation 
    return string


# String Manpulation
for key in final_dict.keys():
    l = final_dict[key]
    for i in range(len(l)):
        if l[i] == 'No Text':
            continue
        elif l[i] == []:
            l[i] = 'No Text'
        else:
            for j in range(len(l[i])):
                l[i][j] = l[i][j].lower()
                l[i][j] = Punctuation(l[i][j])
            l[i] = ["".join(l[i])]
            

# String Matching Levenshtein Distance
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])


# Label Matching of the products
for key in final_dict.keys():
    l = final_dict[key]
    for i in range(len(final_dict[key])):
        string1 = product_details[key]['product_name']
        string1 = string1.lower()
        string1 = Punctuation(string1)
        print(string1)
        string1 = sorted(string1)
        if l[i] == 'No Text':
            continue
        else:
            string2 = sorted(l[i][0])
            if (levenshtein(string1, string2) > 2):
                l[i].append('Mismatched Price Tag')
            else:
                l[i].append('Matched Price Tag')
                
                
                
                
# Storing the price and label name in a combined dictionary
def all_dict(final_dict, detected_obj, dict_price, checking_dict):
    con_dict = {}
    
    list_of_coods = []
    list_of_price = []
    list_of_label_status = []
    
    for key in detected_obj.keys():
        l = detected_obj[key]
        for i in range(len(l)):
            list_of_coods.append(l[i])

            
    for key in final_dict.keys():
        l = final_dict[key]
        for i in range(len(l)):
            if l[i] == 'No Text':
                list_of_label_status.append(l[i])
                continue
            list_of_label_status.append(l[i][1])
            
    
    for key in dict_price.keys():
        l = dict_price[key]
        for i in range(len(l)):
            if l[i] == 'Price is Missing':
                list_of_price.append(l[i])
                continue
            list_of_price.append(l[i][0])
            
                        
    for i in range(len(list_of_coods)):
        temp_dict = {'Price' : '',
                 'Status of Label' : ''}
                
        temp_dict['Status of Label'] = list_of_label_status[i]
        temp_dict['Price'] = list_of_price[i]
        l = list_of_coods[i]
        l = [l[0], l[1] ,l[4], l[5]]
        
        for key, value in checking_dict.items():
            if l == value:
                temp_key = key
        
        con_dict[temp_key] = temp_dict
        
        
    return con_dict


def Merge(dict1, dict2): 
    return(dict2.update(dict1))


final_price_matching = all_dict(final_dict, detected_obj, dict_price, checking_dict)

for key in row_col_dict.keys():
    temp_dict1 = row_col_dict[key]
    if key not in final_price_matching.keys():
        temp_dict = {'Price': 'Price is Missing',
                     'Status of Label': 'No Text'}
        final_price_matching[key] = temp_dict
    temp_dict2 = final_price_matching[key]
    
    Merge(temp_dict1, temp_dict2)
    row_col_dict[key] = temp_dict2
    
print(row_col_dict)
    