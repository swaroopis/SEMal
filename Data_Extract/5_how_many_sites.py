from os import listdir
from os.path import isfile, join


def how_many_sites(encoded, data_folder, ext):
    data = {}
    with open(encoded) as fp:
        fp.readline()
        for line in fp:
            row = list(map(str.strip, line.split(',')))
            data[row[1]] = row[3].strip()

    proteins = [f[0:-9] for f in listdir(data_folder) if isfile(join(data_folder, f)) and f.endswith(ext)]

    sites = 0
    non_sites = 0
    for protein in proteins:
        now = data[protein]
        if len(now) == 0:
            print(now)
            break
        sites += now.count('1')
        non_sites += now.count('0')

    print(sites)
    print(non_sites)


# how_many_sites('./data/Malonylation/Mice/MM_encoded.csv', './data/Malonylation/Mice/HSA/', 'hsb2')
# how_many_sites('./data/Malonylation/Human/HM_encoded.csv', './data/Malonylation/Human/HSA/', 'hsb2')
