##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
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