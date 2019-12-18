import os
from stat import *
from datetime import date, datetime
import re

# @TODO Support for rotated log files - currently using the current year for 'Jan 01' dates.
class LogFileTimeParser(object):
    """
    Extracts parts of a log file based on a start and enddate
    Uses binary search logic to speed up searching

    Common usage: validate log files during testing

    Faster than awk parsing for big log files
    """
    version = "0.01a"

    # Set some initial values
    BUF_SIZE = 4096  # self.handle long lines, but put a limit to them
    REWIND = 100  # arbitrary, the optimal value is highly dependent on the structure of the file
    LIMIT = 75  # arbitrary, allow for a VERY large file, but stop it if it runs away

    line_date = ''
    line = None
    opened_file = None

    @staticmethod
    def parse_date(text, validate=True):
        # Supports Aug 16 14:59:01 , 2016-08-16 09:23:09 Jun 1 2005  1:33:06PM (with or without seconds, miliseconds)
        for fmt in ('%Y-%m-%d %H:%M:%S %f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',
                    '%b %d %H:%M:%S %f', '%b %d %H:%M', '%b %d %H:%M:%S',
                    '%b %d %Y %H:%M:%S %f', '%b %d %Y %H:%M', '%b %d %Y %H:%M:%S',
                    '%b %d %Y %I:%M:%S%p', '%b %d %Y %I:%M%p', '%b %d %Y %I:%M:%S%p %f'):
            try:
                if fmt in ['%b %d %H:%M:%S %f', '%b %d %H:%M', '%b %d %H:%M:%S']:

                    return datetime.strptime(text, fmt).replace(datetime.now().year)
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        if validate:
            raise ValueError("No valid date format found for '{0}'".format(text))
        else:
            # Cannot use NoneType to compare datetimes. Using minimum instead
            return datetime.min

    # Function to read lines from file and extract the date and time
    def read_lines(self):
        """
        Read a line from a file
        Return a tuple containing:
            the date/time in a format supported in parse_date om the line itself
        """
        try:
            self.line = self.opened_file.readline(self.BUF_SIZE)
        except:
            raise IOError("File I/O Error")
        if self.line == '':
            raise EOFError("EOF reached")
        # Remove \n from read lines.
        if self.line[-1] == '\n':
            self.line = self.line.rstrip('\n')
        else:
            if len(self.line) >= self.BUF_SIZE:
                raise ValueError("Line length exceeds buffer size")
            else:
                raise ValueError("Missing newline")
        words = self.line.split(' ')
        # This results into Jan 1 01:01:01 000000 or 1970-01-01 01:01:01 000000
        if len(words) >= 3:
            self.line_date = self.parse_date(words[0] + " " + words[1] + " " + words[2],False)
        else:
            self.line_date = self.parse_date('', False)
        return self.line_date, self.line

    def get_lines_between_timestamps(self, start, end, path_to_file, debug=False):
        # Set some initial values
        count = 0
        size = os.stat(path_to_file)[ST_SIZE]
        begin_range = 0
        mid_range = size / 2
        old_mid_range = mid_range
        end_range = size
        pos1 = pos2 = 0

        # If only hours are supplied
        # test for times to be properly formatted, allow hh:mm or hh:mm:ss
        p = re.compile(r'(^[2][0-3]|[0-1][0-9]):[0-5][0-9](:[0-5][0-9])?$')
        if p.match(start) or p.match(end):
            # Determine Time Range
            yesterday = date.fromordinal(date.today().toordinal() - 1).strftime("%Y-%m-%d")
            today = datetime.now().strftime("%Y-%m-%d")
            now = datetime.now().strftime("%R")
            if start > now or start > end:
                search_start = yesterday
            else:
                search_start = today
            if end > start > now:
                search_end = yesterday
            else:
                search_end = today
            search_start = self.parse_date(search_start + " " + start)
            search_end = self.parse_date(search_end + " " + end)
        else:
            # Set dates
            search_start = self.parse_date(start)
            search_end = self.parse_date(end)
        try:
            self.opened_file = open(path_to_file, 'r')
        except:
            raise IOError("File Open Error")
        if debug:
            print("File: '{0}' Size: {1} Start: '{2}' End: '{3}'"
                  .format(path_to_file, size, search_start, search_end))

        # Seek using binary search -- ONLY WORKS ON FILES WHO ARE SORTED BY DATES (should be true for log files)
        try:
            while pos1 != end_range and old_mid_range != 0 and self.line_date != search_start:
                self.opened_file.seek(mid_range)
                # sync to self.line ending
                self.line_date, self.line = self.read_lines()
                pos1 = self.opened_file.tell()
                # if not beginning of file, discard first read
                if mid_range > 0:
                    if debug:
                        print("...partial: (len: {0}) '{1}'".format((len(self.line)), self.line))
                    self.line_date, self.line = self.read_lines()
                pos2 = self.opened_file.tell()
                count += 1
                if debug:
                    print("#{0} Beginning: {1} Mid: {2} End: {3} P1: {4} P2: {5} Timestamp: '{6}'".
                          format(count, begin_range, mid_range, end_range, pos1, pos2, self.line_date))
                if search_start > self.line_date:
                    begin_range = mid_range
                else:
                    end_range = mid_range
                old_mid_range = mid_range
                mid_range = (begin_range + end_range) / 2
                if count > self.LIMIT:
                    raise IndexError("ERROR: ITERATION LIMIT EXCEEDED")
            if debug:
                print("...stopping: '{0}'".format(self.line))
            # Rewind a bit to make sure we didn't miss any
            seek = old_mid_range
            while self.line_date >= search_start and seek > 0:
                if seek < self.REWIND:
                    seek = 0
                else:
                    seek -= self.REWIND
                if debug:
                    print("...rewinding")
                self.opened_file.seek(seek)
                # sync to self.line ending
                self.line_date, self.line = self.read_lines()
                if debug:
                    print("...junk: '{0}'".format(self.line))
                self.line_date, self.line = self.read_lines()
                if debug:
                    print("...comparing: '{0}'".format(self.line_date))
            # Scan forward
            while self.line_date < search_start:
                if debug:
                    print("...skipping: '{0}'".format(self.line_date))
                self.line_date, self.line = self.read_lines()
            if debug:
                print("...found: '{0}'".format(self.line))
            if debug:
                print("Beginning: {0} Mid: {1} End: {2} P1: {3} P2: {4} Timestamp: '{5}'".
                      format(begin_range, mid_range, end_range, pos1, pos2, self.line_date))
            # Now that the preliminaries are out of the way, we just loop,
            # reading lines and printing them until they are beyond the end of the range we want
            while self.line_date <= search_end:
                # Exclude our 'Nonetype' values
                if not self.line_date == datetime.min:
                    print self.line
                self.line_date, self.line = self.read_lines()
            if debug:
                print("Start: '{0}' End: '{1}'".format(search_start, search_end))
            self.opened_file.close()
        # Do not display EOFErrors:
        except EOFError as e:
            pass
