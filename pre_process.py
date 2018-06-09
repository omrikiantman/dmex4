# TODO - add comment
from os.path import isfile, getsize
import pandas as pd


class PreProcess:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.error_message = ""

    def pre_process(self):
        self.df = pd.read_excel(self.file_path)
        # TODO - check if no values?
        self.complete_missing_values_and_normalize()
        self.aggregate_by_country()

    def verifications(self):
        # verify several tests to see if the file can be pre-processed
        funcs = [self.verify_file_exists, self.verify_file_not_empty, self.verify_file_xlsx]
        for f in funcs:
            self.error_message = f()
            if self.error_message != "":
                return False
        return True

    def verify_file_exists(self):
        # verify that the given path is actually a file and some gibberish
        return "" if isfile(self.file_path) is True else "the given data path is not a valid file"

    def verify_file_not_empty(self):
        # verify if the file can be pre-processed
        return "" if getsize(self.file_path) > 0 else "file is empty"

    def verify_file_xlsx(self):
        # verify if the given file is in xlsx format
        return "" if self.file_path.lower().endswith('.xlsx') else "the given file is not in xlsx format"

    def complete_missing_values_and_normalize(self):
        # fill missing values by their average and standardize them later
        for column in self.df:
            if self.df[column].dtype in ['float64']:
                self.df[column].fillna(self.df[column].mean(), inplace=True)
                self.df[column] = (self.df[column] - self.df[column].mean())/self.df[column].std()
            else:
                continue

    def aggregate_by_country(self):
        # aggregate the records by country, compute mean for each column
        self.df = self.df.groupby('country').mean().reset_index()
        # there no need for the year column
        del self.df['year']
