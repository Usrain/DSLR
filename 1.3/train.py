import math
import pandas as pd
import sys
import csv

def get_values(dataset : dict, key : str) -> tuple[float, float]:
    if not isinstance(key, str):
        raise TypeError("Key must be a string")
    if (key not in dataset):
        raise KeyError("This key does not exist in the dataset")
    total = 0
    count = 0
    for i in dataset[key]:
        if math.isnan(i):
            continue
        total += i
        count += 1
    if count <= 1:
        if math.isnan(dataset[key][0]):
            return (0, 1.0)
        return(dataset[key][0], 1.0)
    mean = total / count
    variance_sum = 0
    for x in dataset[key]:
        if math.isnan(x):
            continue
        variance_sum += ((x - mean) ** 2)
    variance = variance_sum / (count - 1)
    std = math.sqrt(variance)
    return (mean, std)

def Z_score(dataset : dict, key : str) -> list[float]:
    if key == "Hogwarts House":
        return dataset[key]
    mean, std = get_values(dataset, key)
    z_scores = []
    for x in dataset[key]:
        if not isinstance(x, (int, float)) or math.isnan(x):
            z = 0
        else :
            if std == 0:
                z = 0.0
            else :
                z = (x - mean) / std
        z_scores.append(z)
    return z_scores


def lr(dataset : dict, learning_rate : float, epoch : int):
    features = [k for k in dataset.keys() if k != "Hogwarts House"]
    weights = [0.0] * len(features)
    bias = 0.0
    for i in range(0, epoch):


def main():
    threshold = 0.8
    if (len(sys.argv) != 2):
        print("program must be used as train.py dataset")
        sys.exit(-1)
    try :
        with open(sys.argv[1], mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            dataset = {}
            dataset_checker = {}
            for header in headers :
                dataset_checker[header] = [0, 0]
            for row in reader:
                i = 0
                rowlengh = len(row)
                while i < rowlengh:
                    if i >= len(headers):
                        break
                    header = headers[i]
                    if header == "Hogwarts House":
                        if header in dataset:
                            dataset[header].append(row[i])
                        else:
                            dataset[header] = [row[i]]
                        i += 1 
                        continue
                    try :
                        value = float(row[i])
                        if header in dataset:
                            dataset[header].append(value)
                        else :
                            dataset[header] = [value]
                        dataset_checker[header][0] += 1
                    except ValueError:
                        if header in dataset:
                            dataset[header].append(math.nan)
                        else :
                            dataset[header] = [math.nan]
                        dataset_checker[header][1] += 1
                    i += 1
            columns_to_drop = []
            for header in list(dataset.keys()):
                if header == "Hogwarts House":
                    continue
                valid_count = dataset_checker[header][0]
                nan_count = dataset_checker[header][1]
                total_vals = valid_count + nan_count
                
                if total_vals > 0:
                    ratio = valid_count / total_vals
                    if ratio >= threshold:
                        dataset[header] = Z_score(dataset, header)
                    else:
                        columns_to_drop.append(header)
                else:
                    columns_to_drop.append(header)
            for header in columns_to_drop:
                if header == "Hogwarts House":
                    continue
                dataset.pop(header, None)
        print(dataset["Hogwarts House"])
        
    except FileNotFoundError as e:
        print ("file does not exist", e)


if __name__ == "__main__":
    main()