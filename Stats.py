import os
import pandas as pd
import numpy as np


class Stats:
    dataframe = None
    uploads_dir = None

    def __init__(self, filename=os.environ.get('FILENAME')):
        self.dataframe = pd.read_csv(filename)
    
    def store_data(self, file_content, filename):
        filepath = os.path.join('/tmp', filename)
        file_content.save(filepath)
        if os.path.exists(filepath):
            return True
        else:
            return False

    def get_result(self, column_name, return_method):

        def get_most_frequent(column):
            try:
                sub_return_data = list(self.dataframe[column].mode())
            except Exception as e:
                sub_return_data = "Input column name {} is invalid. Use one of the valid column names from the list " \
                                  "below. \n\n{}".format(e, list(self.dataframe.columns)[1:])

            return sub_return_data

        def get_unique_count(column):
            try:
                sub_return_data = self.dataframe[column].nunique()
            except Exception as e:
                sub_return_data = "Input column name {} is invalid. Use one of the valid column names from the " \
                                  "list below. \n\n{}".format(e, list(self.dataframe.columns)[1:])

            return sub_return_data

        if return_method == 'values':
            return_data = get_unique_count(column_name)
        elif return_method == 'common':
            return_data = get_most_frequent(column_name)
        else:
            return_data = "Input return method '{}' is invalid. Use one of the valid return methods from the list " \
                          "below. \n\n['values', 'common']".format(return_method)
        return return_data

    def filter_data(self, filters, return_method=None):
        filtered_data = self.dataframe
        columns = list(filtered_data.columns)
        incorrect_columns_count = 0
        
        def apply_filter(dataframe, column, condition, value):
            if condition == 'eq':
                sub_return_data = dataframe[dataframe[column] == value]
            elif condition == 'leq':
                sub_return_data = dataframe[dataframe[column] <= value]
            elif condition == 'geq':
                sub_return_data = dataframe[dataframe[column] >= value]
            elif condition == 'neq':
                sub_return_data = dataframe[dataframe[column] != value]
            else:
                sub_return_data = dataframe

            return sub_return_data

        for current_filter in filters:
            column_name = current_filter['column']
            equality_condition = current_filter['operator']
            column_value = current_filter['value']

            if column_name in columns:
                filtered_data = apply_filter(filtered_data, column_name, equality_condition, column_value)
            else:
                incorrect_columns_count += 1

        if incorrect_columns_count != len(filters):
            if return_method == 'count':
                return_data = len(filtered_data)
            elif return_method == 'id':
                return_data = filtered_data['Id'].to_list()
            else:
                return_data = dict()
                return_data['total_matches'] = len(filtered_data)
                return_data['matching_ids'] = filtered_data['Id'].to_list()
        else:
            return_data = "Input column names are invalid. Use one of the valid column names from the list below. " \
                          "\n\n{}".format(list(self.dataframe.columns)[1:])
    
        return return_data

    def filter_by_string(self, filters):
        filtered_dataframe = self.dataframe
        incorrect_columns_count = 0
    
        for current_filter in filters:
            column_name = current_filter['column']
            column_value = current_filter['value']

            if column_name in self.dataframe.columns:
                filtered_dataframe = filtered_dataframe[filtered_dataframe[column_name].str.contains(column_value)]
            else:
                incorrect_columns_count += 1

        if incorrect_columns_count != len(filters):
            return_data = len(filtered_dataframe)
        else:
            filtered_columns = self.dataframe.dtypes[self.dataframe.dtypes == np.object]
            return_data = "Input column name is invalid. Use one of the valid column names from the list below. " \
                          "\n\n{}".format(list(filtered_columns))
        return return_data

    def filter_ids(self, ids):

        if isinstance(ids, list) and len(ids) > 0:
            filtered_data = self.dataframe[self.dataframe['Id'].isin(ids)]
            if len(filtered_data) > 0:
                return_data = filtered_data.to_dict()
            else:
                return_data = "Ids in the list {} are not found".format(ids)
        else:
            return_data = "Input should be an array or list of ids"

        return return_data

    def get_sorted_n(self, filters):

        if isinstance(filters, dict) and 'column' in filters and 'limit' in filters:
            column_name = filters['column']
            sort_asc = [True] * len(column_name) if (
                        'order' not in filters or len(column_name) != len(filters['order'])) else filters['order']
            limit = filters['limit']
            if all(column in self.dataframe.columns for column in column_name):
                sorted_data = self.dataframe.sort_values(by=column_name, ascending=sort_asc)
                return_data = sorted_data.head(limit)['Id'].to_list()
            else:
                return_data = "Input column names are invalid. Use one of the valid column names from the list below. " \
                              "\n\n{}".format(list(self.dataframe.columns)[1:])
        else:
            return_data = "Input should be an array or list of ids"

        return return_data
