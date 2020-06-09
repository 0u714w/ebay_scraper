import numpy as np


def generate_average(list_to_average):
    sum_num = 0
    for i in list_to_average:
        if i == 'None':
            i = 0
        else:
            sum_num = sum_num + int(float(i.replace('$', '').replace(',', '')))
    avg = sum_num / len(list_to_average)
    return avg


def detect_outlier(data_1):
    outliers_list = []
    threshold = 3
    mean_1 = np.mean(data_1)
    std_1 = np.std(data_1)
    
    for y in data_1:
        z_score = (y - mean_1) / std_1 
        if np.abs(z_score) > threshold:
            outliers_list.append(y)
    return outliers_list
    

def remove_outlier_from_average(outlier_list, average_list):
    for num in average_list:
        for i in outlier_list:
            if i == num:
                generate_average(average_list.remove(num))
                
    return average_list