import json

def json2csv(csv: list[dict], file: str):
    with open(file, 'w') as f:
        f.write(','.join(csv[0].keys()) + '\n')
        for row in csv:
            f.write(','.join([str(value) for value in row.values()]) + '\n')
