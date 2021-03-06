import pandas as pd
import pybedtools

ssm_files = ['/data/khandekara2/mutation_data/processed_data/MALY_mutation.bed.all.noDuplicates.tsv']
wgbs_files = ['/data/khandekara2/cancer_WGBS/raw_data/MALY_cds.bed']

mutations = []
methylation = []

for wgbs_file, ssm_file in zip(wgbs_files, ssm_files):
    biseq = pd.read_csv(wgbs_file, sep='\t')
    mutation = pd.read_csv(ssm_file, sep='\t')

    biseq_samples = set(biseq['id'].unique())
    mutation_samples = set(mutation['id'].unique())

    #generate list of matching samples in the two types of data
    common_samples = biseq_samples & mutation_samples

    for sample in list(common_samples):
        sub_biseq = biseq[biseq['id'] == sample]
        sub_mutation = mutation[mutation['id'] == sample]

        #write to csv without header and index so files can processed by pybedtools
        sub_biseq.to_csv(sample + '.biseq', sep='\t', index=False, header=False)
        sub_mutation.to_csv(sample + '.mutation', sep='\t', index=False, header=False)

        methylation.append(sample + '.biseq')
        mutations.append(sample + '.mutation')


    #intersect methylation and mutation files matched by sample using Pybedtools wrapper around Bedtools
    for mut, meth in zip(mutations, methylation):
        a = pybedtools.BedTool(mut)
        a.intersect(meth, wa=True, wb=True).saveas('/data/khandekara2/maly_hotspots/' + mut.split('.')[0] + '_overlaps.bed') #finds all mutations in cds where methylation data is available
