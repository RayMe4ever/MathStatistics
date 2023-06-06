import csv

def load_from_csv(file_name: str):
    data = []
    with open(file_name) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";")
        for row in spamreader:
            data.append(float(row[0]))
    return data

def load_text(filename):
    with open(filename, 'r') as file:
        values = [float(line) for line in file]
    return values

def load_octave(file_name: str):
    a, b, w = load_text(file_name)
    return float(a), float(b), w