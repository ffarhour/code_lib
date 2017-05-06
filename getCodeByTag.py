import os,re,sys,argparse   #built-in
import pandas as pd

class bcolors:
    """Used to implement ANSI colors without the need to remember the numbers.
    Does not contain any methods. Only contains variables.
    Usage: simply concatenate bcolors.<color> at the start of string to be printed,
        and bcolors.ENDC at the end of the string, to color the string with the
        specified color.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main(argv):
    print(bcolors.HEADER + "Script to find to search for the specific function/class/piece of code you desire in the library" + bcolors.ENDC)

    # argparse
    parser = argparse.ArgumentParser(description='Get Code Snippet by Tags')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--lang', '-l', type=str, metavar='<language>', choices=["cpp","python","java"], help='cpp, python, java etc.', required=True)
    requiredNamed.add_argument('--tags', '-t', type=str, metavar='<space-separated string of tags>', help='the tags to search for', required=True)

    args = parser.parse_args()
    print(args)

    # create an array of tags to match
    tags_array = args.tags.split()

    # check if language path exists
    language_path = os.path.join(os.getcwd(),"lib",args.lang)
    if(not os.path.isdir(language_path)):
        print(bcolors.FAIL + "Language does not exist in library" + bcolors.ENDC)
        return;
    else:
        # define var for max number of tag matches, and its file_name
        max_tag_matches = 0
        folder_name = ""
        # iterate through tags and find the best match
        for root, dirs, files in os.walk(language_path):
            for file in files:
                # find tag files
                if(file=="tags"):
                    match_counter = 0
                    f = open(os.path.join(root,file), "r")
                    tag_line = f.readline().split()
                    for elements in tag_line:
                        for to_be_matched in tags_array:
                            if(elements==to_be_matched): #if a tag matches
                                match_counter += 1
                    # If the tags matched are higher than previous max match
                    if(match_counter > max_tag_matches):
                        max_tag_matches = match_counter
                        folder_name = root
        if(max_tag_matches>0):
            print(bcolors.OKGREEN + "SUCCESS, found the best match for your tags" + bcolors.ENDC)
            for filename in os.listdir(folder_name):
                if(filename!="tags"):
                    with open(os.path.join(folder_name,filename)) as f:
                        print(bcolors.UNDERLINE + "YOUR CODE:" + bcolors.ENDC)
                        print(bcolors.OKBLUE + f.read() + bcolors.ENDC)
                    with open(os.path.join(folder_name,filename)) as f:
                        content = f.read().splitlines()
                    df=pd.DataFrame(content)
                    df.to_clipboard(index=False,header=False, sep=None)
                    print(bcolors.OKGREEN + "Code copied to clipboard" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "FAIL: no matches for your search" + bcolors.ENDC)

if __name__ == "__main__":
    main(sys.argv)
