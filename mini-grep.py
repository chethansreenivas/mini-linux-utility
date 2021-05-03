import os
import argparse

# output fields to display
OUTPUT_FIELDS = ["No", "Line"]
# output formats for print
OUTPUT_FORMAT_1 = "{:<5} {:<400}"
OUTPUT_FORMAT_2 = "{:<400}"


class MiniGREP():
    """
    Serach pattern in the givens files and prints
    line number and the line where the pattern is found

    Usage:
        minigrep = MiniGREP()
        file = sample2.txt
        pattern = "linux"
        output = minigrep.get_matches(file, pattern)
        minigrep.process_output(output)
    """

    def process_output(self, output, line_number):
        """
        To print line_number,line matching pattern

        Args:
             output(tuple(int,str)): tuple(line number, line)
                                     where pattern is found
             line_number(bool): flag to print line numbers

        return None
        """
        print("-"*70)
        if not line_number:
            print(OUTPUT_FORMAT_2.format(OUTPUT_FIELDS[1]))
        else:
            print(OUTPUT_FORMAT_1.format(OUTPUT_FIELDS[0], OUTPUT_FIELDS[1]))
        for item in output:
            if not line_number:
                print(OUTPUT_FORMAT_2.format(item[1]))
            else:
                print(OUTPUT_FORMAT_1.format(item[0], item[1]))
        print("-"*70)

    def get_matches(self, path, pattern):
        """
        To process files and extract the lines matching given pattern

        Args:
            path(str): file name or absolute path to the file
            pattern(str): pattern to search

        return [(int,str)]: (line number, line) from files matching pattern
        """
        isExist = os.path.exists(path)
        # to check if the given file path exixts
        if not isExist:
            print(f"Error! Path {path} doesn't exist.\
                  Please provide valid file path")
            exit()
        # to check if the given path is a valid regular file
        isFile = os.path.isfile(path)
        if not isFile:
            print(f"Error! File: {path} is not valid.\
                  Please provide absolute file path")
            exit()
        with open(path) as myFile:
            for num, line in enumerate(myFile, 1):
                # stripping unwanted characters
                line = line.rstrip('/n')
                if pattern in line:
                    yield (num, line)


if __name__ == "__main__":
    # create args parser object
    parser = argparse.ArgumentParser(description='Search files for pattern')
    parser.add_argument('-q', action="store_true", default=False,
                        dest='no_line_num',
                        help='to skip printing line number in \
                        file where pattern is found')
    parser.add_argument('-e', '--pattern', action='store', type=str,
                        dest='pattern',
                        help="pattern to search. Examples: -e Linux")
    parser.add_argument('-f', '--files', action='store', default=[],
                        dest='files', nargs='*', type=str,
                        help="absolute paths.\
                        Examples: -f /u/chethan/utils /u/akash/NLP")
    # parsing CLI args
    args = parser.parse_args()
    minigrep = MiniGREP()
    line_num = not(args.no_line_num)
    search_pattern = args.pattern
    files = args.files
    # get files from standard input if not given through args
    if not files:
        input_files = input(f"Please proved files to \
                            search pattern: {search_pattern}\n")
        # parse input files
        files = input_files.split()
        if not files:
            print("Error! Couldn't parse files. please provide files seprated \
                  by " "(space)) Ex: /u/chethan/NLP /u/chethan/NLP")
            exit()
    # Iterating files to search pattern
    for file in files:
        print("#" * 70)
        print(f"File: {file}")
        print("#" * 70)
        output = []
        # Fetching (line_no, line) matching pattern
        output = minigrep.get_matches(file, search_pattern)
        # Print output
        minigrep.process_output(output, line_num)
    print("#" * 70)
