import abc
import os
from os import listdir
from os.path import isfile, join, basename,isdir

import pandas as pd


class AbstractBulkRunner(metaclass=abc.ABCMeta):
    def __init__(self):
        self.success = 0
        self.failure = 0

    def read_all_directories(self,root_directory):
        onlydir = [os.path.join(root_directory, f) for f in listdir(root_directory) if
                     isdir(join(root_directory, f))]
        print("All Sub Directories")
        print(onlydir)
        return onlydir

    def read_all_train_files(self, folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        print(onlyfiles)
        return onlyfiles

    def write_dataframe_to_excel(self, dataframe, sheet_name, folder_path, file_name):
        destination = os.path.join(folder_path, file_name)
        writer = pd.ExcelWriter(destination)
        dataframe.to_excel(writer, sheet_name)
        writer.save()

    def write_dataframes_to_single_excel(self, dataframe_one, dataframe_second, sheet_name_one, sheet_name_second,
                                         folder_path,
                                         file_name):
        destination = os.path.join(folder_path, file_name)
        writer = pd.ExcelWriter(destination)
        dataframe_one.to_excel(writer, sheet_name_one)
        dataframe_second.to_excel(writer, sheet_name_second)
        writer.save()

    def write_dataframes_to_excel(self, dataframes, folder_path, file_name):
        count = 0
        output_folder = os.path.join(folder_path, 'bulk_cluster_classifier_output')
        destination = os.path.join(output_folder, file_name + '.xlsx')
        writer = pd.ExcelWriter(destination)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for dataframe in dataframes:
            count += 1
            dataframe.to_excel(writer, 'Sheet' + str(count))
        writer.save()

    def write_json_output(self, folder_path, content_to_write, file_name):
        output_folder = os.path.join(folder_path, 'generated_output')
        output_file = os.path.join(output_folder, file_name + '.json')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open(output_file, mode='w') as out_file:
            out_file.write(content_to_write)

    def write_html_output(self, folder_path, content_to_write, file_name):
        output_folder = os.path.join(folder_path, 'html_generated_output')
        output_file = os.path.join(output_folder, file_name + '_h1_h2_tagged.html')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open(output_file, mode='wb') as out_file:
            out_file.write(content_to_write)
            out_file.flush()

    def write_failure_files(self, source, folder_path):
        destination = os.path.join(folder_path, 'failed_files')
        file = basename(source)
        out = os.path.join(destination, file)
        if not os.path.exists(destination):
            os.makedirs(destination)
        os.rename(source, out)
        self.failure += 1

    def move_successful(self, successful, folder_path):
        for source in successful:
            destination = os.path.join(folder_path, 'successful_files')
            file = basename(source)
            out = os.path.join(destination, file)
            if not os.path.exists(destination):
                os.makedirs(destination)
            os.rename(source, out)
            self.success += 1

    @abc.abstractmethod
    def executor(self, folder_path,client_name):
        pass
