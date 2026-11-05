import csv
import sys
import math


def get_values(dataset : dict, key : str) -> tuple[int, float, float, float, float, float, float, float]:
    if not isinstance(key, str):
        raise TypeError("Key must be a string")
    if (key not in dataset):
        raise KeyError("This key does not exist in the dataset")
    count = len(dataset[key])
    if count <= 1:
        return (1, dataset[key][0], dataset[key][0], dataset[key][0], dataset[key][0], dataset[key][0], dataset[key][0], dataset[key][0])
    total = 0
    for i in dataset[key]:
        total += i
    mean = total / count
    variance_sum = 0
    max = dataset[key][0]
    min = dataset[key][0]
    for x in dataset[key]:
        variance_sum += ((x - mean) ** 2)
        if (x < min):
            min = x
        elif (x > max):
            max = x
    variance = variance_sum / (count - 1)
    std =  math.sqrt(variance)
    sortedvals = sorted(dataset[key])
    first_q = sortedvals[int(0.25 * (count - 1))]
    second_q = sortedvals[int(0.5 * (count - 1))]
    third_q = sortedvals[int(0.75 * (count - 1))]
    return (count, mean, std, min, first_q, second_q, third_q, max)


def print_describe(dataset : dict, dataset_checker : dict):
    treshold = 0.9
    metrics_names = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
    raw_columns = list(dataset.keys())
    columns = []
    for col in raw_columns:
        valid = dataset_checker[col][0]
        invalid = dataset_checker[col][1]
        total = valid + invalid
        if total > 0 and (valid / total) > treshold:
            columns.append(col)
    if not columns:
        print("Error: No numeric columns found.")
        return
    row_format = "{:<7} " + " ".join(["{:>12}"] * len(columns))
    header_format = "{:<7} " + " ".join(["{:>12}"] * len(columns))
    truncated_columns = [col[:12] for col in columns]
    print(header_format.format("", *truncated_columns))
    for i, stat_name in enumerate(metrics_names):
        row_values = []
        for col in columns:
            if ((dataset_checker[col][0] / (dataset_checker[col][0] + dataset_checker[col][1])) > treshold):
                stats = get_values(dataset, col)
                val = stats[i]
                if isinstance(val, (int, float)):
                    row_values.append(f"{val:.6f}")
                else:
                    row_values.append(str(val))
        print(row_format.format(stat_name, *row_values))



def main():
    if (len(sys.argv) != 2):
        print("program must be used as describe.py dataset")
        sys.exit(-1)
    try :
        with(open(sys.argv[1], mode='r') as file):
            reader = csv.reader(file)
            headers = next(reader)
            dataset = {}
            dataset_checker = {}
            i = 0
            for header in headers :
                dataset_checker[headers[i]] = [0, 0]
                i = i + 1
            for row in reader:
                i = 0
                rowlengh = len(row)
                while (i < rowlengh):
                    if i < len(headers):
                        try :
                            value = float(row[i])
                            if (headers[i] in dataset):
                                dataset[headers[i]].append(value)
                            else :
                                dataset[headers[i]] = []
                                dataset[headers[i]].append(value)
                            dataset_checker[headers[i]][0] += 1
                        except ValueError:
                            dataset_checker[headers[i]][1] += 1
                            pass
                    i += 1
        print_describe(dataset, dataset_checker)
    except FileNotFoundError as e:
        print ("file does not exist", e)

if (__name__ == "__main__"):
    main()