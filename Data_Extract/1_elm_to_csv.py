import pandas as pd


def elm_to_csv(input, output_h, output_m):
    needed_data = ['PLMD ID', 'Uniprot Accession', 'Position', 'Sequence']
    human = {}
    mice = {}

    with open(input) as fp:
        lines = fp.readlines()
        header = lines[0].split('\t')
        print(header)
        for head in header:
            if head in needed_data:
                human[head] = []
                mice[head] = []

        for (i, line) in enumerate(lines):
            if i > 0:
                splitedData = line.split('\t')
                species = splitedData[5]
                for (j, val) in enumerate(splitedData):
                    if header[j] in needed_data:
                        if species.lower() == 'homo sapiens':
                            human[header[j]].append(val)
                        if species.lower() == 'mus musculus':
                            mice[header[j]].append(val)

        human_df = pd.DataFrame(human)
        human_df.to_csv(output_h, sep=",")

        mice_df = pd.DataFrame(mice)
        mice_df.to_csv(output_m, sep=",")

        print("Human ", human_df.shape)
        print("Mice ", mice_df.shape)


elm_to_csv('./data/Malonylation/Malonylation.elm', './data/Malonylation/Human/Human_Malonylation.csv', './data/Malonylation/Mice/Mice_Malonylation.csv')