[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
# pansplit
a command line tool for pangenome creation based on metadata 

As more bacterial sequence data is available for analysis, there will undoubtebly be a need to construct pangenomes in ways that match certain metadata that is associated with that data.

I've encountered this problem in my research and thought it would be nice to have a tool that can arbitrate the construction of pangenomes based on metadata. pansplit is my way of addressing this problem (grateful for lockdown to give me more free time to embark on this type of thing).


### Installation
Primarily, you need to have 3 things to have pansplit not whine:
1) python
2) roary - for pangenome inference
3) pandas - for manipulating the metadata file

Users might also find it helpful to just use conda and create the environment to use pansplit from the yaml file within this repository. I would advise this route.

### Example Usage
I provided a test data file within the repo to instantly get some practice with pansplit. You will find the following:
1) GFF Files - these are one of the necessary files needed to make pansplit run. They contain information about the genome annotations. Files created by prokka should do just the trick here
2) sample_meta.csv - a CSV file containing the metadata associated with the GFF files. It's important that there is a 'Sample' column that has a one-to-one mapping between the GFF files and the elements of the column. It looks like this:

Sample | M1 |	M2 |	M3
------ | -- | --- | ---
00-17MIDNRdeerMontm_S23_L001.	| A |	C |	X
00-1MIDNRdeerAlc_S5_L001. |	A	| D	| Y
00-21MIDNRdeerOts_S14_L001. |	A	| C	| Z
00-26MIDNRdeerAlp_S12_L001.	| A	| D	| Z
00-27MIDNRdeerAlp_S27_L001.	| A	| C	| Z
00-28MIDNRdeerEmm_S2_L001.	| B	| C	| X
00-29MIDNRdeerAlc_S37_L001.	| B	| D	| Y
00-2MIDNRdeerOsco_S32_L001.	| B	| C	| X
00-32MIDNRdeerOts_S19_L001.	| B	| C	| Z
00-33MIDNRdeerPI_S7_L001.	| B	| C	| Y


With that we are off to the races. On your command line, you will want to type something to this effect:
```
python /path/to/pansplit.py -m /path/to/sample_meta.csv -o name_of_output_directory -v A -c M1 -v D -c M2 -t <number of threads>
```
### Feature Wishlist
* More complex filtering options
* Figure out how to properly edit GFF files to exclude/include certain features

### Thank you!
I hope people get good use out of this mini tool I made. Please leave issues to suggest how I can make this tool even better!

## Noah A. Legall, University of Georgia Institute of Bioinformatics
