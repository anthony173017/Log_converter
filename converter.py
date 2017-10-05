import numpy
import os.path as locate
import argparse
import glob
import pandas

parser = argparse.ArgumentParser(description="Takes in n distances for a log and filters them out. Run this program as follows:\npython converter.py [the distances you want to select split by spaces]\nThen it will write those new files out for you.")

parser.add_argument('-path', type=str, nargs=1, help="Changes the path of the master log to whatever you type")
parser.add_argument('-filename', type=str, nargs=1, help="If you want to change the file name that's output when the program is done, just add this flag (don't add the csv at the end)", default="data")
parser.add_argument('-zones', type=int, nargs='+', help="The zones you want separated by spaces", choices=range(1,12), default=range(1,12))
parser.add_argument('-whitelist', type=int, nargs='+', help="The zones you specify here will not be affected by the filtering process", choices=range(1,12), default=range(7,12))
parser.add_argument('distances', type=int, nargs='+', help="Distances that you want separated by spaces", choices=[0,1,2,5,10,20,30,40,50,60])
args = parser.parse_args()

text = None
if args.path is None:
    print("User specified no path, so assuming the log is in the current directory, which is " + locate.dirname(locate.realpath(__file__)) + "...")
    files = glob.glob("*log.*")
    n = len(files)
    if n == 0:
        print("There's no log files located in this directory. You are running this program in the wrong folder, your files are named incorrectly (they have to end in log but can be any type of file extension), or your files are not located in the same directory. Either move them to the same one as this program or use the '-path' flag to specify where they are. Run 'python converter.py -h' to see full usage.")
        exit()
    elif n != 1:
        print("There's more than one log file possible here. Which one do you want?")
        for i in range(n):
            print("File " + str(i) + ": " + files[i])
        while True:
            try: x = int(input("Type the number of the file you want to process:"))
            except:
                print("Bad input: not an integer")
                continue
            if x >= n or x < 0:
                print("Bad input: not a valid number that I gave you")
                continue
            else:
                n = x
                break
    else: n = 0
    try: text = pandas.read_csv(files[n])
    except:
        print("Error opening your file, is it a correctly formatted CSV?")
        exit()
else:
    print("Looking for file located at \"" + args.path[0] + "\"...")
    try:
        text = pandas.read_csv(args.path[0])
    except:
        print("File was not found or was not properly formatted. Make sure at the end of your path you add the file name, putting the directory its in isn't enough")
        exit()

text.columns = ["Date", "Zone", "Distance","Comment","M","1","2","3","4","5","6"]
		
print("Only including these zones:", args.zones)
print("Only including these distances:", args.distances)
print("Whitelisting these zones nomatter the conditions:", args.whitelist)

text = text[(text.Zone.isin(args.zones) & text.Distance.isin(args.distances)) | text.Zone.isin(args.whitelist)]
file_to_write = args.filename+ ".csv"

try: text.to_csv(open(file_to_write, 'w'), index=False)
except:
	print("Error writing file. Some sort of error happened trying to write to the directory specified")
	exit()

print("Wrote file " + file_to_write)
print("Completed.")