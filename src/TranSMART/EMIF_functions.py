import csv
import os
import tmtk
from collections import OrderedDict

class InvalidInputException(Exception):
    pass


class IncorrectDataException(Exception):
    pass


class Clinical_params(object):
    rest_attributes = ("SECURITY_REQUIRED", "TOP_NODE", "STUDY_ID", "XTRIAL_FILE",
                       "TAGS_FILE", "RECORD_EXCLUSION_FILE", "USE_R_UPLOAD", "TOP_NODE_PREFIX")

    def __init__(self, filename, batch=False, all_none=True):
        if batch:
            study_directory = os.path.dirname(os.path.abspath(filename))
            self.directory = os.path.join(study_directory, "clinical")
        else:
            self.directory = os.path.dirname(os.path.abspath(filename))
        if all_none:
            for attribute in self.rest_attributes:
                setattr(self, attribute, None)

        with open(filename, 'r') as handle:
            for line in handle.readlines():
                if line == "" or line.startswith("#"):
                    continue
                line = line.strip()
                variable, value = line.split("=")
                if variable == "COLUMN_MAP_FILE":
                    self.COLUMN_MAP_FILE = value
                    if not os.path.exists(self.COLUMN_MAP_FILE):
                        msg = "Column mapping file {} doesn't exist.\n".format(self.COLUMN_MAP_FILE)
                        msg += "Check the clinical.params for the correct value.\n"
                        msg += "Or check if the setup matches your setting for batch mode (-b)\n"
                        msg += "Provided the option if your study is in this setup"
                        raise IncorrectDataException(msg)
                elif variable == "WORD_MAP_FILE":
                    if value == "":
                        continue
                    self.WORD_MAP_FILE = value
                    if not os.path.exists(self.WORD_MAP_FILE):
                        msg = """Word mapping file {} doesn't exist.\n".format(self.WORD_MAP_FILE)
                                Check the clinical.params for the correct value.\n
                                or check if the setup matches your setting for batch mode (-b)\n
                                Provided the option if your study is in this setup"""
                        raise IncorrectDataException(msg)
                elif variable in self.rest_attributes:
                    setattr(self, variable, value)
                else:
                    msg = "{} doesn't have the attribute {}".format("Clinical Params object", variable)
                    raise IncorrectDataException(msg)

        if not hasattr(self, "COLUMN_MAP_FILE"):
            msg = "COLUMN_MAP_FILE not in {}".format(filename)
            raise IncorrectDataException(msg)
        if not hasattr(self, "WORD_MAP_FILE"):
            setattr(self, "WORD_MAP_FILE", None)

    @property
    def COLUMN_MAP_FILE(self):
        return os.path.join(self.directory, self._COLUMN_MAP_FILE)

    @COLUMN_MAP_FILE.setter
    def COLUMN_MAP_FILE(self, value):
        if value in (None, ""):
            msg = "COLUMN_MAP_FILE must be a file and not None or empty"
            raise IncorrectDataException(msg)
        else:
            self._COLUMN_MAP_FILE = value

    @property
    def WORD_MAP_FILE(self):
        if self._WORD_MAP_FILE == None:
            return None
        else:
            return os.path.join(self.directory, self._WORD_MAP_FILE)

    @WORD_MAP_FILE.setter
    def WORD_MAP_FILE(self, value):
        self._WORD_MAP_FILE = value

def get_mapped_diction(unique_values, data_file_column, word_map, strip_empty=False):
    mapped_values = dict()
    for unique_value in unique_values:
        if unique_value == '' and strip_empty:
            continue
        if data_file_column in word_map:
            if unique_value in word_map[data_file_column]:
                mapped_values[unique_value]=word_map[data_file_column][unique_value]
            else:
                mapped_values[unique_value]=None
        else:
            mapped_values[unique_value]=None
    return mapped_values


def get_header(filename):
    with open(filename, 'r') as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)

    return header


def get_reader(filename, return_header=False):
    handle = open(filename, 'r')
    reader = csv.reader(handle, delimiter="\t")
    try:
        header = next(reader)
    except csv.Error:
        handle.close()
        handle = open(filename, 'rU')
        reader = csv.reader(handle, delimiter='\t')
        header = next(reader)
    if return_header:
        return header, reader, handle
    else:
        return reader, handle

def check_column_mapping_uniqueness(filename):
    allowed_dublicates = ("OMIT", "SUBJ_ID")

    reader, handle = get_reader(filename)
    path_labels = set()
    errors = set()
    for row in reader:
        path = row[1]
        label = row[3]
        if label in allowed_dublicates:
            continue

        unique_set = (path, label)
        if unique_set not in path_labels:
            path_labels.add((path, label))
        else:
            errors.add((row[0], row[2], path, label))

    handle.close()

    if errors:
        print("Duplicate in column mapping:")
        for i, error in enumerate(errors):
            data_filename, column, path, label = error
            print("\t{:2d}: Label: '{}' with path '{}'".format(i + 1, label, path))
            print("\t    In data file {} at column {}".format(data_filename, column))
            print("")
        raise IncorrectDataException()

    return True

def get_column_mapping(filename, label_path_key=True, check=True):
    """
    Convert to Pandas
    :param filename:
    :param label_path_key:
    :param check:
    :return:
    """
    if check:
        check_column_mapping_uniqueness(filename)

    result = OrderedDict()

    reader, handle = get_reader(filename)

    for row in reader:
        data_filename = row[0]
        path = row[1]
        column = row[2]
        label = row[3]
        if label_path_key:
            key = (label, path)
            result[key] = (data_filename, column)
        else:
            key = (data_filename, column)
            result[key] = (label, path)

    handle.close()
    return result

def get_unique_value_per_column(data_filename, filter_empty=True):
    """
    Convert to pandas
    :param data_filename:
    :param filter_empty:
    :return:
    """
    result = dict()
    handle = open(data_filename, 'r')
    base = os.path.basename(data_filename)

    try:
        reader = csv.reader(handle, delimiter="\t")
        next(reader)  # header
    except csv.Error:
        handle = open(data_filename, 'rU')
        reader = csv.reader(handle, delimiter="\t")
        next(reader)

    table = zip(*[row for row in reader])
    for i, column in enumerate(table):
        unique = set()
        for value in set(column):
            # value = transform_to_numerical(value)
            unique.add(value)

        if filter_empty and "" in unique:
            unique.remove("")

        result[(base, str(i + 1))] = unique
    handle.close()
    return result

def get_word_mapping(filename):
    """
    :keyword: Should be converted to pandas
    :return: dict (datafile, column){value:new_value,
                                     value:new_value}
    """
    handle = open(filename, 'r')
    try:
        reader = csv.reader(handle, delimiter="\t")
    except csv.Error:
        handle = open(filename, 'rU')
        reader = csv.reader(handle, delimiter="\t")
    try:
        next(reader)  # header

        result = OrderedDict()
        for i, row in enumerate(reader):
            if len(row) != 4:
                msg = "Row {!s} in file {} doesn't have 4 columns".format(i + 2, filename)
                raise HyveException(msg)
            key = (row[0], row[1])
            if key not in result:
                result[key] = dict()
            # value = transform_to_numerical(row[2])
            value = row[2]
            result[key][value] = row[3]

        handle.close()
    except:
        print
        filename
        raise
    return result


def get_key_value_diction(filename: str, header=True, delimiter="\t")-> dict:
    result = dict()

    handle = open(filename, 'r')
    reader = csv.reader(handle, delimiter=delimiter)
    if header:
        next(reader)

    for i, row in enumerate(reader):
        if header:
            row_number = i + 2
        else:
            row_number = i + 1

        if row[0][0] == "#":
            continue
        try:
            result[row[0]] = row[1]
        except IndexError:
            msg = "At {!s} in {} the row doesn't have 2 values, but {}".format(row_number, os.path.basename(filename),
                                                                               len(row))
            handle.close()
            raise InvalidInputException(msg)

    handle.close()

    return result


def check_filename(*files)-> None:
    errors = list()
    for filename in files:
        if filename and not os.path.exists(filename):
            errors.append(filename)

    if errors:
        msg = "The following filenames don't exists:\n"
        msg += "\n".join(errors)
        raise InvalidInputException(msg)


def transform_to_numerical(value):
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    return value


def get_clinical_params_from_folder(folder, batch):
    tree = os.walk(folder)

    study_clinial_params = dict()
    for folder_name, subfolders, files in tree:
        if ".git" in folder_name:
            continue

        if "clinical.params" in files:
            dirs = os.path.abspath(folder_name).split("/")

            if dirs[-1] != "clinical":
                study = dirs[-1]
            else:
                study = dirs[-2]
            filename = os.path.join(folder_name, "clinical.params")
            clinical_params = Clinical_params(filename, batch)
            study_clinial_params[study] = clinical_params
    return study_clinial_params


def is_categorical(values, strict=True, remove_empty=False):
    num_values = {transform_to_numerical(value) for value in values}

    if remove_empty and "" in num_values:
        num_values.remove("")
    if strict:
        if any([isinstance(value, str) for value in num_values]):
            return True
        else:
            return False
    else:
        numerical = [value for value in num_values if not isinstance(value, str)]
        percentage_numerical = len(numerical) / len(num_values)
        if percentage_numerical >= 0.8:
            return False
        else:
            return True

def create_column_mapping_file(result, data_filename, outputfile, omit=True, column_number=6):
    columns = ["Filename", "Category_Code (tranSMART)", "Column", "DataLabel", "data_label_src", "ControlVocab_cd"]
    with open(outputfile,'w') as handle:
        if column_number == 6:
            template = "{filename}\t{path}\t{column}\t{label}\t\t\n"
        elif column_number == 7:
            columns.append("Data_type")
            template = "{filename}\t{path}\t{column}\t{label}\t\t\t\n"
        else:
            msg = "Column number is not 6 or 7 but {} for data_filename".format(column_number)
            raise InvalidInputException(msg)
        handle.write("\t".join(columns)+"\n")
        for key, column in sorted(result.items(), key=lambda key_column_tuple: key_column_tuple[1]):
            label, path = key
            if path.split("+")[0] == "????":
                if omit:
                    path = ""
                    label = "OMIT"
                else:
                    path = "????"
            string = template.format(filename = os.path.basename(data_filename),
                                     path = path,
                                     column = column,
                                     label = label)
            handle.write(string)


def create_xtrial_mapping_file(result, output_xtrial, modify=True):
    with open(output_xtrial, 'w') as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(("study_prefix", "xtrial_prefix"))
        for key in result.keys():
            label, path = key
            if path.startswith("?") or label == "OMIT":
                continue
            if label in ("SUBJ ID", "SUBJ_ID"):
                continue
            complete_path = "\{}+{}".format(path, label)
            if modify:
                complete_path = complete_path.replace("+", "\\")
                new_path = complete_path.replace("_", " ")
            else:
                if label in ("AGE", "GENDER"):
                    new_path = "\{}+{}".format(path, label.title())
                new_path = complete_path

            writer.writerow((new_path, new_path))


def exclude_studies(studies, exclude):
    check_filename(exclude)
    with open(exclude, 'r') as handle:
        excluded_studies = [line.strip() for line in handle.readlines() if not line.startswith("#")]
    for study in excluded_studies:
        if study in studies:
            del (studies[study])
        else:
            msg = "Study {} not found".format(study)
            raise InvalidInputException(msg)

    print("Excluded {}".format(", ".join(excluded_studies)))

    return studies


def get_studies(folder, exclude=None):
    tree = os.walk(folder)

    studies = OrderedDict()
    for folder_name, subfolders, files in tree:
        if "study.params" in files:
            study_name = os.path.basename(folder_name)
            study_params = os.path.join(folder_name, "study.params")
            studies[study_name]=study_params

    print("Found the following studies: {}".format(", ".join(studies)))

    if exclude:
        studies = exclude_studies(studies, exclude)

    for study_name, study_params in studies.items():
        studies[study_name]=tmtk.Study(study_params)

    return studies
