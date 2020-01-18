def get_file_name(op_folder, protein_name):
    return op_folder + '/' + protein_name + '.seq'


def get_fasta(input, output):
    with open(input, 'r') as fp:
        now = ""
        protein_name = ""
        for (i, line) in enumerate(fp):
            if i % 2 == 0:
                protein_name = line[1:-1]
                now += line
            if i % 2 == 1:
                now += line
                with open(get_file_name(output, protein_name), "w") as op:
                    op.write(now)
                now = ""


# get_fasta('./data/Malonylation/Human/HM_cdhit.fasta', './data/Malonylation/Human/protein-seq')
# get_fasta('./data/Malonylation/Mice/MM_cdhit.fasta', './data/Malonylation/Mice/protein-seq')
