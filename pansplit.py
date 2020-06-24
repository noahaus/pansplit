# pan-split
# this software is a command line tool to create pangenomes based on metadata queries
# input: directory of GFF files + metadata csv
# output: directories that have pangenomes based on user specified arguments.

### packages - and why they are there

import sys # use to access arguments
import os # use in order to call commands from the terminal script is called in
import glob # grabs files by name and puts them in a list
import re # we can do regular expression features with this
import time # for time stamps
import pandas as pd # will be used for the table querying.
import argparse #user friendly argument creation
import psutil as ps #let's use this to know the amount of available cores are
### functions

logger = lambda message: "[{}] {}".format(time.strftime('%m/%d/%Y %H:%M:%S'),message)

def roary_run(list_of_samples,output_name):
    gff_list = list(map(lambda element: element + ".gff",list_of_samples))
    with open('temp.txt','w') as temp:
        temp.write('\n'.join(gff_list))

    output_dir = "{}_pangenome_directory".format(output_name)
    os.system("mkdir {}".format(output_dir))
    os.system("ls | grep -f temp.txt | xargs cp -t {}".format(output_dir))
    os.chdir(output_dir)
    os.system("roary -v -p {} *.gff".format(args.threads))
    os.chdir("../")
    os.system("rm temp.txt")


### arguments

parser = argparse.ArgumentParser()
parser.add_argument('-m','--metadata',dest='meta',help='Provide the path to the metadata csv file.')
parser.add_argument('-o','--output',dest='out',help='The name used for the output directories/database/results.')
parser.add_argument('-v','--value',dest='value',action='append',nargs='+',help='filter the data to create a pangenome by the specified metadata. use this parameter with -x to specify the metadata column.')
parser.add_argument('-c','--column',dest='column',action='append',nargs='+',help='the corresponding list of filters need to have a corresponding column')
parser.add_argument('-t','--threads',dest='threads',default=ps.cpu_count()/2,help='number of threads to create pangenomes')

args = parser.parse_args()

### logic

gff_files = sorted(glob.glob("*.gff"))

# check if the inputs are even present

if len(gff_files) > 1:
    print(logger("GFF files are present and obtained."))
else:
    print(logger("ERROR - there are either no GFF files or too few to warrant this program being useful"))
    sys.exit(0)

if not args.out:
    print(logger("ERROR - no output file specified."))
    sys.exit(0)
else:
    print(logger("output specified and will be denoted with \'{}\'".format(args.out)))

if not args.meta:
    print(logger("ERROR - no metadata file specified."))
    sys.exit(0)
else:
    print(logger("metadata provided from {} file".format(args.meta)))

# use pandas to read in the metadata file
try:
    metadata_file = pd.read_csv("{}".format(args.meta))
    if "Sample" not in metadata_file.columns:
        print(logger("ERROR - there is no column defined as \'Sample\' in the CSV file"))
        sys.exit(0)
    else:
        print(logger("metadata successfully uploaded using pandas"))
except:
    print(logger("ERROR - something is wrong in your metadata file. is it actually a CSV?"))
    sys.exit(0)

# check if the column and value pairs are equal
try:
    if len(args.value) != len(args.column):
        print(logger("ERROR - it appears you supplied an unequal amount of values and columns"))
        sys.exit(0)
    else:
        print(logger("every value has a column that it corresponds to"))
except:
    print(logger("ERROR - you didn't provide any value or column information"))
    sys.exit(0)

iter_pairs = zip(args.column,args.value)
count = 0
query = ""
for i,j in iter_pairs:
    if count == 0:
        query = "{} == {}".format(i[0],"\'{}\'".format(j[0]))
    else:
        query = query + " & {} == {}".format(i[0],"\'{}\'".format(j[0]))
    count = count + 1
try:
    filtered_pd = metadata_file.query(query)
    print(logger("filtering the metadata now"))
except:
    print(logger("ERROR - something is wrong with the filtering of the metadata"))
    sys.exit(0)
print(logger("here are the columns that satisfy your search:\n"))
print(filtered_pd)
sample_list = filtered_pd['Sample'].tolist()
roary_run(sample_list,args.out)
