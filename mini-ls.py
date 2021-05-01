import os
import stat
import time
import pwd
import pprint
import types
import argparse


class MiniLS():
    """
    """
    def _format(self, output_dict):
        str_fmt = "{:<20} {:<15} {:<10} {:<30}"
        keys = list(output_dict.keys())
        values = list(output_dict.values())
        print(str_fmt.format(keys[0],keys[1],keys[2],keys[3]))
        print(str_fmt.format(values[0],values[1],values[2][0],values[3]))

    def process_output(self, output):
        """
        """
        for item in output:
            if not isinstance(item, types.GeneratorType):
                self._format(item)
            else:
                process_output(item)

    def _extract_info(self, file):
        """
        """
        file_details = {}
        file_info = file.stat()
        file_details["name"] = file.name
        file_details["permissions"] = stat.filemode(file_info.st_mode)
        # output: pwd.struct_passwd(pw_name='root', pw_passwd='x', pw_uid=0,
        #          pw_gid=0, pw_gecos='root', pw_dir='/root', pw_shell='/bin/bash')
        file_details["owner"] = (pwd.getpwuid(file_info.st_uid).pw_name, pwd.getpwuid(file_info.st_uid).pw_uid)
        file_details["last_modified"] = time.ctime(file_info.st_mtime)
        return file_details

    def extract_recursive(self, path, recursive=True):
        """
        """
        print(f"Directory: {path}")
        try:
            scan_output =  os.scandir(path)
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
    parser = argparse.ArgumentParser(description='List information about the paths')
    parser.add_argument('-r', action="store_true", default=False,
                        dest='recursive', help='to run recursively on all directories')
    parser.add_argument('-f','--files', action='store', default=[os.getcwd()],
                        dest='files',nargs='*', type=str, help="absolute paths Examples: -f /u/chethan/redhat /u/eliad/redhat")
    args = parser.parse_args()
    minils = MiniLS()
    print(args.files)
    print(args.recursive)
    recursive_flag = args.recursive
    for file in args.files:
        print("#"* 70)
        print(f"Path: {file}")
        print("#"* 70)
        output = minils.extract_recursive(file, recursive_flag)
        minils.process_output(output)
        print("#"* 70)
