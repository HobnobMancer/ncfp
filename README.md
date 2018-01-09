# README.md - `ncbi_cds_from_protein`

This repository contains code for a script that identifies and writes the corresponding nucleotide sequences for each protein in an input multiple sequence file to be used, for example, in backthreading coding sequences onto protein alignments for phylogenetic analyses. It uses the NCBI accession or UniProt gene name (as appropriate) to identify source nucleotide sequences in the NCBI databases, and writes them to a file.

Downloaded results are cached locally to an SQLite database for ease of recovery.

## Usage

Providing an input file of protein sequences as `<INPUT>.fasta`, and writing output to the directory `<OUTPUT>`, while specifying a user email to NCBI of `<EMAIL>` will generate two files: `<OUTPUT>/ncfp_aa.fasta` and `<OUTPUT>/ncfp_nt.fasta`.

```bash
ncfp <INPUT>.fasta <OUTPUT> <EMAIL>
```

The file `<OUTPUT>/ncfp_aa.fasta` contains the amino acid sequences for all input proteins for which a corresponding nucleotide coding sequence could be identified, in FASTA format.

The file `<OUTPUT>/ncfp_nt.fasta` contains nucleotide coding sequences, where they could be found, for all the input proteins, in FASTA format.

Any input protein sequences for which a corresponding nucleotide sequence cannot be recovered, for any reason, are placed in the file `<OUTPUT>/skipped.fas`.


### NCBI format protein input

By default, `ncfp` will assume that sequences are in NCBI format (as though downloaded from an NCBI search) with the accession for each sequence as the sequence identifier string. 

```bash
ncfp <INPUT>.fasta <OUTPUT> <EMAIL>
```

The input FASTA sequence identifiers (the string immediately following the `>` symbol) for each protein sequence are retained in the nucleotide sequence output. For example:

```
>XP_004520832.1 kunitz-type serine protease inhibitor homolog dendrotoxin I-like [Ceratitis capitata]
MRTKFVLVFALIVCVLNGLGEAQRPAHCLQPHPQGVGRCDMLISGFFYNSERNECEQWTE
EGCRVQGGHTYDFKEDCVNECIEIN
```

is recovered as:

```
>XP_004520832.1 coding sequence
ATGAGAACTAAATTTGTTTTGGTATTCGCGCTCATTGTTTGTGTACTCAACGGTTTAGGT
GAAGCGCAAAGACCAGCACATTGCTTACAACCACATCCACAAGGAGTTGGCCGTTGTGAT
ATGCTTATCAGTGGTTTCTTCTATAACTCGGAGCGTAATGAGTGCGAGCAATGGACAGAG
GAGGGCTGCCGTGTGCAGGGTGGGCACACATACGATTTCAAAGAAGATTGTGTAAATGAG
TGCATTGAAATTAATTAA
```

### UniProt format protein input

To specify that the input file contains protein sequences derived from UniProt, use the `-u` or `--uniprot` argument. 

```bash
ncfp -u <INPUT>.fasta <OUTPUT> <EMAIL>
ncfp --uniprot <INPUT>.fasta <OUTPUT> <EMAIL>
```

This instructs `ncfp` to use the provided *gene name* in the description string of the UniProt sequence as the identifier, located using the regular expression `(?<=GN=)[^\s]+`. This gene name is used as the identifier in the nucleotide sequence output.

```
>tr|D8LFH3|D8LFH3_ECTSI Glucosylceramidase, family GH30 OS=Ectocarpus siliculosus GN=Esi_0015_0036 PE=4 SV=1
MRGYNRIPEGASPGESDAQGAREEGNVRTPLRSSSGSAAEGQGGETRNRRLAVAVPLGVL
GVLGVLLITSGGGGRRLRPEPEAGSPASFESQHSVAGVSVFESSFHDGTRLDQGFPAPAS
LKQVIAVCAERGVSGTVVVESDDKLQEIIGFGGAFTDAATINFFKLPEDVQEQVLDAYFG
PNGIEYSVGRIPMGSCDFSVEQYSFDEVPGDYNLTHFDDGVEKDTAQRIPMLLSALARRE
DLKLFTSPWSPPAWMKEPKDGVQSMIESALPQGLLADPGVHAAWALFFSRFISAYKEQGV
DLWGLTIQNESENPGPWEACVYTPSSQAKFIRDHLGPVIRRDHPDVKIMAFDHNRDHLVT
WAEEMMSNEETAQYVDGMAFHWYVASWNRLLDGSMGWGALNTTHNLLSGRDKFILSTESC
NCPNVDHSLEGGWKRAEHTLHEMIADVNSWSTGWVDWNLMLSYDGGPNHAGNLCDTPIVS
NENHTDVIFQPMFYSIGHMSKFAQPGARRLKSHVTGLYQNGGSGPSTALAGYEATLYGCE
GSVRQSWEMSATGRISLADNFGAQYDWFQPLCLSKDISESFKSVNLVPCDSDQAGTFVYD
QDSGRIALQADASSPPDADPQTVADAEDPVVSGSTESVCLDVLDGSTDDGVVLTLNPCDL
ESTSEDTSSGQRWEFAEAKSGDGGGGSLVSAATGRCMTAGWPFFTGAAFEMSDASKDRYG
KDYAVVLLNEAEEPVEFDLSFPSEGFSVRAIIGPRAIQTILA
```

is recovered as:

```
>Esi_0015_0036 coding sequence
ATGCGGGGCTACAACAGGATCCCGGAGGGCGCTTCACCAGGGGAGTCGGATGCACAGGGC
GCGCGCGAGGAGGGCAACGTGCGTACCCCCCTCCGCAGCAGCAGCGGCTCTGCGGCAGAG
GGACAAGGCGGTGAGACCCGTAACAGGAGGCTCGCCGTTGCCGTACCTCTCGGAGTTCTC
GGCGTTCTCGGGGTTCTTTTGATCACGTCGGGGGGTGGGGGTCGACGGCTGCGGCCGGAG
CCGGAAGCTGGCTCGCCCGCCAGCTTTGAAAGCCAGCACTCGGTTGCTGGGGTGTCGGTG
TTCGAGAGCTCCTTTCACGATGGGACAAGGCTTGACCAGGGCTTCCCTGCCCCGGCGAGC
TTGAAACAGGTCATAGCGGTCTGCGCAGAGAGGGGCGTGTCTGGGACGGTGGTGGTGGAG
TCGGACGACAAGCTGCAGGAGATTATCGGATTCGGGGGAGCTTTCACCGACGCCGCCACG
ATAAACTTCTTCAAGCTGCCGGAGGATGTTCAGGAGCAGGTGTTGGACGCATACTTCGGA
CCCAACGGCATCGAGTACAGCGTTGGCCGCATCCCCATGGGCAGCTGCGACTTCAGCGTG
GAGCAGTACAGCTTCGACGAAGTGCCGGGAGACTACAACCTCACGCACTTCGATGATGGC
GTGGAGAAGGACACCGCTCAGAGGATCCCGATGCTCCTCTCGGCCCTCGCGCGCCGGGAG
GACCTGAAGCTCTTCACGTCTCCGTGGAGCCCTCCCGCATGGATGAAGGAGCCGAAAGAC
GGAGTTCAGAGCATGATCGAGAGCGCTCTGCCGCAGGGACTGCTGGCGGACCCCGGGGTG
CACGCTGCGTGGGCACTCTTCTTCAGCCGCTTTATATCGGCCTACAAGGAACAGGGGGTG
GATTTGTGGGGGCTGACGATCCAGAATGAGTCTGAGAACCCGGGTCCGTGGGAGGCTTGC
GTGTACACGCCCTCATCTCAGGCTAAATTCATCCGCGACCACCTCGGTCCCGTCATCCGG
AGGGACCACCCGGACGTGAAGATCATGGCCTTCGACCACAACAGAGACCACCTGGTAACG
TGGGCGGAGGAGATGATGAGCAACGAAGAGACGGCTCAGTACGTCGACGGCATGGCCTTC
CACTGGTACGTGGCTTCGTGGAACAGGCTGCTGGACGGCAGCATGGGCTGGGGCGCTCTC
AACACGACCCACAACCTGCTGAGCGGAAGAGACAAGTTCATCCTCTCGACGGAGAGCTGC
AACTGCCCCAACGTGGACCACTCCCTGGAGGGGGGCTGGAAGAGGGCAGAACACACGCTG
CACGAAATGATCGCCGACGTCAACAGCTGGTCCACTGGATGGGTGGACTGGAACCTGATG
CTCAGTTATGACGGTGGACCGAACCACGCTGGCAACCTGTGCGACACTCCCATCGTCAGC
AACGAGAACCACACGGACGTCATCTTCCAGCCGATGTTCTACTCCATCGGCCACATGTCG
AAGTTTGCCCAGCCCGGAGCGAGGCGGCTCAAGAGTCACGTAACGGGGCTGTACCAGAAC
GGTGGGAGCGGGCCTTCCACAGCCTTGGCCGGCTACGAGGCCACCCTGTACGGGTGCGAG
GGCAGCGTGCGCCAGAGCTGGGAGATGTCGGCGACGGGCAGGATATCCCTGGCGGACAAC
TTCGGTGCCCAGTACGACTGGTTCCAGCCCTTGTGCCTGTCGAAAGACATTTCGGAATCC
TTCAAGTCCGTTAACTTGGTGCCCTGCGACTCCGACCAAGCCGGCACGTTCGTCTATGAC
CAAGACAGCGGCCGCATCGCCCTGCAGGCCGACGCCTCCTCCCCCCCCGACGCGGACCCC
CAAACCGTGGCCGACGCCGAGGATCCCGTAGTTTCAGGATCGACGGAGTCAGTCTGCCTG
GATGTGCTCGACGGGTCTACCGATGACGGGGTGGTGCTAACCCTTAACCCGTGCGATCTG
GAATCCACATCAGAGGACACTAGCAGCGGTCAGCGATGGGAATTTGCTGAGGCGAAATCC
GGCGACGGGGGAGGGGGGAGCCTGGTGTCCGCCGCCACCGGCCGGTGCATGACCGCCGGG
TGGCCCTTCTTCACCGGGGCCGCCTTCGAGATGAGCGACGCCTCCAAGGACCGCTACGGC
AAGGACTACGCGGTGGTCCTGCTCAACGAGGCGGAGGAACCGGTGGAGTTCGACCTCTCC
TTCCCTTCGGAGGGGTTCTCGGTCAGGGCGATCATCGGGCCCCGCGCCATCCAGACCATC
CTCGCCTAA
```


### Stockholm domain format input

UniProt and other sources use Stockholm format to indicate that an amino acid sequence represents a portion of a protein (such as a domain). Sequences in this format can be recovered using the `-s` or `--stockholm` argument.

```bash
ncfp -u -s <INPUT>.fasta <OUTPUT> <EMAIL>
ncfp --uniprot --stockholm <INPUT>.fasta <OUTPUT> <EMAIL>
```

The Stockholm format location information is not preserved in the nucleotide sequence output, and gaps are not preserved. For instance,

```
>tr|B7G6L2|B7G6L2_PHATC/43-112 [subseq from] Predicted protein OS=Phaeodactylum tricornutum (strain CCAP 1055/1) GN=PHATRDRAFT_48282 PE=4 SV=1
-----------------------------SLCV-EVAGA-SQD---DGASIFQGDCN-dG
NKHQVFDFipaPG---TdsgFHRIRA--SHSN-KCLGVADGAL--APG-AEVVQ-
```

is recovered as

```
>PHATRDRAFT_48282 coding sequence
TCGCTCTGCGTGGAGGTGGCTGGAGCGAGCCAAGACGACGGGGCCTCCATATTTCAAGGG
GATTGTAATGACGGAAACAAGCATCAAGTCTTCGACTTCATTCCTGCTCCCGGTACAGAC
AGCGGTTTTCATCGAATTCGAGCCTCGCACTCCAACAAGTGCCTTGGCGTGGCTGATGGG
GCTTTAGCACCTGGAGCTGAGGTAGTGCAA
```