import pandas as pd

def load_from_csv(file_name: str):
    data = pd.read_csv(file_name, encoding='1251', sep=';')
    return data

def load_text(filename):
    with open(filename, 'r') as file:
        values = [float(line) for line in file]
    return values

def load_octave(file_name: str):
    a, b, w = load_text(file_name)
    return float(a), float(b), w