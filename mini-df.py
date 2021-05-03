import os
import argparse
import shutil

# output fields to display
OUTPUT_FIELDS = ["Total Space", "Free Space", "Used Space"]
# output fields format
OUTPUT_FORMAT = "{:<15} {:<15} {:<15}"
# supported human readable size formats
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
SIZE_REF = 1000


class MiniDF():
    """
    Lists disk usage information of the given path

    Usage:
        minidf = MiniDF()
        file = "/u/chethan/tmp/"
        #to get output in human readable sizes
        output1 = minidf.disk_usage(file)
        minidf.process_output(output1, human_readable=True)
        #to get output in bytes
        output2 = minidf.disk_usage(file)
        minidf.process_output(output2, human_readable=False)

    """
    def _format(self, output_values):
        """
        To print the given values

        Args:
            output_values(list): disk usage info

        return none
        """
        print(OUTPUT_FORMAT.format(output_values[0],
                                   output_values[1],
                                   output_values[2]))

    def _human_readable(self, size_in_bytes):
        """
        To convert bytes to human readable output

        Args:
           size_in_bytes(int): usage in bytes

        return (str): human readable sizes
        """
        index = 0
        while size_in_bytes >= SIZE_REF:
            size_in_bytes /= SIZE_REF
            index += 1
        if not index > len(SIZE_UNITS) - 1:
            return "{:.3f} {}".format(size_in_bytes, SIZE_UNITS[index])
        return "{:.3f} {}".format(size_in_bytes * SIZE_REF, SIZE_UNITS[-1])

    def process_output(self, memory_usage, human_readable):
        """
        To print and process disk usage output

        Args:
            memory_usage(named tuple): tuple with disk usage info
                                       Ex: usage(total=8237965312,
                                                 used=0, free=8237965312)
            human_readable(bool): flag to print usage in human readable format

        return none
        """
        print("-"*70)
        self._format(OUTPUT_FIELDS)
        total_space = memory_usage.total
        free_space = memory_usage.free
        used_space = memory_usage.used
        if not human_readable:
            output = [total_space,
                      free_space,
                      used_space]
        else:
            output = [self._human_readable(total_space),
                      self._human_readable(free_space),
                      self._human_readable(used_space)]
        self._format(output)
        print("-"*70)

    def disk_usage(self, path):
        """
        To fetch disk usage information of the gicen path

        Args:
            path(str): absolute path of file

        return memory_usage(named tuple): disk usage information
                                         Ex: usage(total=8237965312,
                                                   used=0, free=8237965312)
        """
        try:
            memory_usage = shutil.disk_usage(path)
        except Exception as e:
            print(f"{e}\n Please pass valid file path")
            exit()
        return memory_usage


if __name__ == "__main__":
    # create args parser object
    parser = argparse.ArgumentParser(description='List disk usage information')
    parser.add_argument('-H', action="store_true", default=False,
                        dest='human_readable',
                        help='to get disk usage information\
                        in human readable format')
    parser.add_argument('-f', '--files', action='store', default=[os.getcwd()],
                        dest='files', nargs='*', type=str,
                        help="absolute paths.\
                        Ex: -f /u/chethan/redhat /u/eliad/redhat")
    # parsing CLI args
    args = parser.parse_args()
    minidf = MiniDF()
    human_readable = args.human_readable
    for file in args.files:
        print("#" * 70)
        print(f"File: {file}")
        print("#" * 70)
        output = minidf.disk_usage(file)
        minidf.process_output(output, human_readable)
        print("#" * 70)
