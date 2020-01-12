from progressbar import Bar
import datetime
import exifread
import os
import re

MONTHS = {'01': '01 - Jan', '02': '02 - Feb', '03': '03 - Mar', '04': '04 - Apr', '05': '05 - May', '06': '06 - Jun',
          '07': '07 - Jul', '08': '08 - Aug', '09': '09 - Sep', '10': '10 - Oct', '11': '11- Nov', '12': '12 - Dec'}


def add_date(file_path):
    """Adds date YYYY-MM-DD_ to beginning of file name of photo based on EXIF data"""

    assert os.path.isfile(file_path), 'Not a file: ' + file_path
    abs_path = os.path.abspath(file_path)

    dir_name = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    already_dated = len(re.findall("^\d{4}-\d{2}-\d{2}_", file_name)) == 1

    if not already_dated:
        date = check_date(file_name)
        if date and is_valid(date):
            new_name = date + file_name.lstrip('_')
            new_path = dir_name + '/' + new_name
        else:
            tag = get_exif_tag(file_path, 'EXIF DateTimeOriginal')
            tags = re.findall("\d{4}:\d{2}:\d{2}", tag.values) if tag else []
            if len(tags) == 1:
                date_str = tags[0].replace(':', '-')
                new_name = date_str + '_' + file_name.lstrip('_')
                new_path = dir_name + '/' + new_name
            else:
                new_path = dir_name + '/unknown_date/' + file_name

        try:
            os.rename(file_path, new_path)
        except FileNotFoundError:
            os.mkdir(dir_name + '/unknown_date')
            os.rename(file_path, new_path)
        except FileExistsError as e:
            raise AssertionError(str(e))


def check_date(file_name):
    """Checks for date in file name"""

    check = re.findall("\d{4}-\d{2}-\d{2}", file_name)
    if len(check) == 1:
        return check[0] + '_'

    check = re.findall("\d{8}_", file_name)
    if len(check) == 1:
        return check[0][:4] + '-' + check[0][4:6] + '-' + check[0][6:]

    check = re.findall("\d{8}-", file_name)
    if len(check) == 1:
        return check[0][:4] + '-' + check[0][4:6] + '-' + check[0][6:8] + '_'


def date_files(input_dir):
    """Calls add_date on all files in a directory (shallow)"""

    assert os.path.isdir(input_dir), 'Not a directory: ' + input_dir
    names = os.listdir(input_dir)
    progress_bar = Bar('Adding dates to files', max=len(names))

    for name in names:
        if os.path.isfile(input_dir + '/' + name):
            add_date(input_dir + '/' + name)
        progress_bar.next()
    progress_bar.finish()


def get_exif_tag(file_path, exif_tag):
    """Gets specified EXIF tag data from file and returns it"""

    assert os.path.isfile(file_path), 'Not a file: ' + file_path

    with open(file_path, 'rb') as f:
        try:
            tags = exifread.process_file(f, stop_tag=exif_tag)
        except IndexError:
            return None
    try:
        return tags[exif_tag]
    except KeyError:
        return None


def is_valid(date_str):
    """Checks if date string in the format YYYY-MM-DD_ is a valid date"""

    try:
        image_date = datetime.date.fromisoformat(date_str[:-1])
    except ValueError:
        return False

    current = (datetime.datetime.now() + datetime.timedelta(days=1)).date()

    if image_date > current or image_date.year < 1800:
        return False

    return True


def sort_items(input_dir):
    """Sorts renamed items into folders based on date"""

    assert os.path.isdir(input_dir), 'Not a directory: ' + input_dir
    names = os.listdir(input_dir)
    progress_bar = Bar('Sorting files', max=len(names))

    for name in names:
        if os.path.isfile(input_dir + '/' + name):
            date_strings = re.findall("\d{4}-\d{2}-\d{2}_*", name)
            if len(date_strings) == 1:
                y, m, d = date_strings[0][:4], date_strings[0][5:7], date_strings[0][8:10]

                try:
                    os.rename(input_dir + '/' + name, input_dir + '/' + y + '/' + MONTHS[m] + '/' + d + '/' + name)
                except FileNotFoundError:
                    if not os.path.exists(input_dir + '/' + y):
                        os.mkdir(input_dir + '/' + y)
                    if not os.path.exists(input_dir + '/' + y + '/' + MONTHS[m]):
                        os.mkdir(input_dir + '/' + y + '/' + MONTHS[m])
                    if not os.path.exists(input_dir + '/' + y + '/' + MONTHS[m] + '/' + d):
                        os.mkdir(input_dir + '/' + y + '/' + MONTHS[m] + '/' + d)
                    os.rename(input_dir + '/' + name, input_dir + '/' + y + '/' + MONTHS[m] + '/' + d + '/' + name)
                except FileExistsError as e:
                    raise AssertionError(str(e))

            else:
                try:
                    os.rename(input_dir + '/' + name, input_dir + '/unsorted/' + name)
                except FileNotFoundError:
                    os.mkdir(input_dir + '/unsorted')
                    os.rename(input_dir + '/' + name, input_dir + '/unsorted/' + name)
                except FileExistsError as e:
                    raise AssertionError(str(e))

        progress_bar.next()
    progress_bar.finish()
