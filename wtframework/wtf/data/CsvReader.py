'''
Created on Feb 11, 2013

@author: davidlai
'''
import csv

class CsvReader(object):
    """
    Provides an iterator for accessing CSV records.
    """
    _csv_reader = None
    _headers = None
    _file = None
    
    def __init__(self, file_path):
        "Constructor"
        self._file = open(file_path, 'rb')
        
        self._csv_reader = csv.reader(self._file, delimiter=',', dialect='excel')
        self._headers = self._csv_reader.next()

        
    def next(self):
        "Gets next entry as a dictionary."
        try:
            entry = {}
            row = self._csv_reader.next()
            for i in range(0,len(row)):
                entry[self._headers[i]] = row[i]
            
            return entry
        except Exception as e:
            #close our file when we're done reading.
            self._file.close()
            raise e
    

    def __del__(self):
        # close our file if it's not closed yet.
        try:
            self._file.close()
        except:
            pass