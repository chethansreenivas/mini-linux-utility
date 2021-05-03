import os
import stat
import time
import pwd
import types
import argparse

# output fields to display
OUTPUT_FIELDS = ["name", "permissions", "owner", "last_modified"]
# output fields format
OUTPUT_FORMAT = "{:<20} {:<15} {:<10} {:<30}"


class MiniLS():
    """
    Lists information on the given path/directory

    Usage:
        minils = MiniGREP()
        file = "/home/chethan/NLP"
        # to list all the files across all directories recursively
        output1 = minils.extract_recursive(file, True)
        minils.process_output(output1)
        # to list only files and directories in the given path
        output2 = minils.extract_recursive(file, False)
        minils.process_output(output2)

    """
    def _format(self, output_values):
        """
        To print file details

        Args:
            output_values(list(str)): list of file info

        return none
        """
        print(OUTPUT_FORMAT.format(output_values[0],
                                   output_values[1],
                                   output_values[2][0],
                                   output_values[3]))

    def process_output(self, output):
        """
        To process ouput and print file info

        Args:
            output(list(dict)): file information
                            ex:[{'name': 'mini-ls.py',
                                'permissions': '-rw-r--r--',
                                'owner': ('chethan', 1000),
                                'last_modified': 'Fri Apr 30 22:21:42 2021'
                                }]

        return none
        """
        print("-"*70)
        print(OUTPUT_FORMAT.format(OUTPUT_FIELDS[0],
                                   OUTPUT_FIELDS[1],
                                   OUTPUT_FIELDS[2],
                                   OUTPUT_FIELDS[3]))
        for item in output:
            if not isinstance(item, types.GeneratorType):
                values = list(item.values())
                self._format(values)
            else:
                self.process_output(item)
        print("-"*70)

    def _extract_info(self, file):
        """
        To extract infor from scanned files

        Args:
            file(scandir): scanned file object

        return file_details(dict): file details: ["name",
                                                  "permissions",
                                                  ("owner", owner_id),
                                                  "last_modified"]
        """
        file_details = {}
        file_info = file.stat()
        file_details["name"] = file.name
        file_details["permissions"] = stat.filemode(file_info.st_mode)
        # output: pwd.struct_passwd(pw_name='root', pw_passwd='x', pw_uid=0,
        #      pw_gid=0, pw_gecos='root', pw_dir='/root', pw_shell='/bin/bash')
        file_details["owner"] = (pwd.getpwuid(
                                file_info.st_uid).pw_name,
                                pwd.getpwuid(file_info.st_uid).pw_uid)
        file_details["last_modified"] = time.ctime(file_info.st_mtime)
        return file_details

    def extract_recursive(self, path, recursive=True):
        """
        To extract file info on the given path

        Args
            path(str): directory path to liist files
            recursive(bool=True): to extract all the files across all
                                  the directories at given path

        yield list(dict): returns file info with required fields
        """
        # print(f"FILE: {path}")
        try:
            scan_output = os.scandir(path)
        except Exception as e:
            print(f"{e}\n Please pass valid file path")
            exit()
        for entry in scan_output:
            if not recursive:
                yield self._extract_info(entry)
            else:
                if entry.is_file():
                    yield self._extract_info(entry)
                else:
                    yield self.extract_recursive(entry.path, recursive)


if __name__ == "__main__":
    # create args parser object
    parser = argparse.ArgumentParser(description='List information about \
                                     the paths')
    parser.add_argument('-r', action="store_true", default=False,
                        dest='recursive',
                        help='to run recursively on all directories')
    parser.add_argument('-f', '--files', action='store', default=[os.getcwd()],
                        dest='files', nargs='*', type=str,
                        help="absolute paths.\
                             Examples: -f /u/chethan/redhat /u/eliad/redhat")
    # parsing CLI args
    args = parser.parse_args()
    minils = MiniLS()
    recursive_flag = args.recursive
    for file in args.files:
        print("#" * 70)
        print(f"File: {file}")
        print("#" * 70)
        output = minils.extract_recursive(file, recursive_flag)
        minils.process_output(output)
        print("#" * 70)
