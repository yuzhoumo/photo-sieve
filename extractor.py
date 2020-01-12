from interface import log
from progressbar import Bar
from progressbar import Counter
import hashlib
import os
import shutil


def check_duplicates(input_path):
    """Shallow check if there are duplicate files (based on sha1 hash) in the same directory"""

    assert os.path.isdir(input_path), 'Input path must be a valid directory'

    if not os.path.exists(input_path + '/duplicates'):
        os.mkdir(input_path + '/duplicates')

    hashes, BLOCK_SIZE = {}, 65536
    names = sorted(os.listdir(input_path))
    names.reverse()
    progress_bar = Bar('Checking for duplicates', max=len(names))
    log_data = 'Duplicates (duplicate filename -> sha1 hash = original file):\n'

    for name in names:
        if os.path.isfile(input_path + '/' + name):
            hasher = hashlib.sha1()

            with open(input_path + '/' + name, 'rb') as file:
                buffer = file.read(BLOCK_SIZE)
                while len(buffer) > 0:
                    hasher.update(buffer)
                    buffer = file.read(BLOCK_SIZE)
            result = hasher.hexdigest()

            if result in hashes:
                try:
                    os.rename(input_path + '/' + name, input_path + '/duplicates/' + name)
                    log_data += '\n' + name + ' -> ' + result + ' = ' + hashes[result]
                except FileExistsError as e:
                    raise AssertionError(str(e))
            else:
                hashes[result] = name
        progress_bar.next()
    log(log_data, input_path + '/duplicates/log.txt', 0)
    progress_bar.finish()


def extract_files(input_path, output_path):
    """Recursively copies all files from input path to output path"""

    assert os.path.isdir(input_path), 'Not a directory: ' + input_path
    assert os.path.isdir(output_path), 'Not a directory: ' + output_path
    assert len(os.listdir(output_path)) == 0, 'Output directory is not empty.'
    assert input_path != output_path, 'Input and output directories cannot be the same.'

    def extract(input_dir):
        for file_name in os.listdir(input_dir):
            path = input_dir + '/' + file_name

            if os.path.isfile(path):
                if not os.path.exists(output_path + '/' + file_name):
                    shutil.copy2(path, output_path + '/' + file_name)
                else:
                    count = 1
                    file_name, ext = split_file_name(file_name)
                    while os.path.exists(output_path + '/' + file_name + ' (' + str(count) + ')' + ext):
                        count += 1
                    shutil.copy2(path, output_path + '/' + file_name + ' (' + str(count) + ')' + ext)
                file_counter.index += 1
                file_counter.update()
            elif os.path.isdir(path):
                extract(path)

    file_counter = Counter('Copying files:')
    extract(input_path)
    file_counter.finish()


def filter_files(input_dir, file_types):
    """Filters specified file types into a separate folder"""

    assert os.path.isdir(input_dir), 'Not a directory: ' + input_dir

    names = os.listdir(input_dir)
    progress_bar = Bar('Filtering file types', max=len(names))

    for name in names:
        if os.path.isfile(input_dir + '/' + name) and split_file_name(name)[1].lower() not in file_types:
            try:
                os.rename(input_dir + '/' + name, input_dir + '/non_image/' + name)
            except FileNotFoundError:
                os.mkdir(input_dir + '/non_image')
                os.rename(input_dir + '/' + name, input_dir + '/non_image/' + name)
            except FileExistsError as e:
                raise AssertionError(str(e))
        progress_bar.next()
    progress_bar.finish()


def split_file_name(name):
    """Splits file name into name and extension"""

    for i in range(-1, -len(name) - 1, -1):
        if name[i] == '.':
            return name[:i], name[i:]
    return name, ''
