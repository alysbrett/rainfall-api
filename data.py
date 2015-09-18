import csv

INFILE = "rainfall.txt"

def get_data():
    data = []
    with open(INFILE) as datafile:
        reader = csv.reader(datafile, delimiter='\t')
        next(reader)   #skip headers
        for row in reader:
            data.append(row)
    return data

def get_year_data(year):
    data = None
    with open(INFILE) as datafile:
        reader = csv.reader(datafile, delimiter='\t')
        next(reader)   #skip headers
        for row in reader:
            if row[0] == str(year):
                del row[0]
                data = []
                for val in row:
                    data.append(float(val))
    return data

def get_year_data_dict(year):
    data = None
    with open(INFILE) as datafile:
        reader = csv.DictReader(
            datafile,
            delimiter='\t',
            quoting=csv.QUOTE_NONNUMERIC,
            dialect="excel")
        for row in reader:
            if row["Year"] == year:
                data = row
                del data["Year"]
    return data


def get_month_labels():

    with open(INFILE) as datafile:
        reader = csv.reader(datafile, delimiter='\t')
        header_row = next(reader)
        del header_row[0]  #first col is year - not a month label
    return header_row

