from datetime import datetime
import extractor
import organizer
import os

FILE_FILTER = {'.3gp', '.amv', '.arw', '.avi', '.bmp', '.dng', '.flv', '.gif', '.heic', '.heif', '.hvec', '.jpeg',
               '.jpg', '.m4v', '.mkw', '.mov', '.mp4', '.mpeg', '.mpg', '.png', '.psd', '.rmvb', '.svg', '.svi',
               '.tif', '.webm', '.webp', 'tiff'}


def enter_directory(message, error_message):
    """Prompts user to enter a valid directory"""

    directory = input(message)
    while not os.path.exists(directory):
        print(error_message + directory)
        directory = input(message)
    return directory


def log(data, log_location, mode):
    """Writes data to a log file (mode 0: log to file, mode 1: log to file and print to console)"""

    assert not os.path.isdir(log_location), 'Error, log path is a directory: ' + log_location
    assert mode == 0 or mode == 1, 'Invalid log mode: ' + str(mode)

    with open(log_location, 'a') as f:
        f.write('\n' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '\n')
        f.write(data)

    if mode == 1:
        print('\n' + data)


def yes_no_input(message):
    """Prompts user to enter yes or no"""

    return True if input(message).lower() in ('yes', 'y') else False


def main():
    run = True
    while run:
        print('\nPhotoSeive v1.0.0 by PPanda\n')

        # Menu options
        print('Options:')
        print('1. Copy and auto-sort the photos and videos inside a folder and its sub-folders')
        print('2. Extract all files from folder and sub-folders to output folder')
        print('3. Filter out all duplicate files from folder (does not check sub-folders)')
        print('4. Filter out all photos and videos from folder (does not check sub-folders)')
        print('5. Add dates to photos and videos in a folder (does not check sub-folders)')
        print('6. Sort files with dates added in the format: "YYYY-MM-DD_" (does not check sub-folders)')
        print('7. Exit program\n')
        choice = input('Select an option by typing its corresponding number: ').strip()
        print()
        try:
            if choice == '1':  # Copy and auto-sort the photos and videos inside a folder and its sub-folders
                input_dir = enter_directory('Enter a photo directory to sort: ', 'Error, invalid directory: ')
                output_dir = enter_directory('Enter an output directory: ', 'Error, invalid directory: ')
                assert os.path.abspath(input_dir) != os.path.abspath(output_dir),\
                    'Input and output directories cannot be the same.'
                assert len(os.listdir(output_dir)) == 0, 'Output directory must be empty.'
                print()

                extractor.extract_files(input_dir, output_dir)
                extractor.check_duplicates(output_dir)
                extractor.filter_files(output_dir, FILE_FILTER)

                organizer.date_files(output_dir)
                organizer.sort_items(output_dir)
                print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))

            elif choice == '2':  # Extract all files from folder and sub-folders to output folder
                input_dir = enter_directory('Enter a photo directory to sort: ', 'Error, invalid directory: ')
                output_dir = enter_directory('Enter an output directory: ', 'Error, invalid directory: ')
                assert os.path.abspath(input_dir) != os.path.abspath(output_dir), \
                    'Input and output directories cannot be the same.'
                assert len(os.listdir(output_dir)) == 0, 'Output directory must be empty.'
                print()

                extractor.extract_files(input_dir, output_dir)
                print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))

            elif choice == '3':  # Filter out all duplicate files from folder (does not check sub-folders)
                cont = yes_no_input('This choice will reorder the contents of the directory. Continue? (y/n): ')
                if cont:
                    output_dir = enter_directory('Enter a directory: ', 'Error, invalid directory: ')
                    print()
                    extractor.check_duplicates(output_dir)
                    print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))
                else:
                    print('Action cancelled.')

            elif choice == '4':  # Filter out all photos and videos from folder (does not check sub-folders)
                cont = yes_no_input('This choice will reorder the contents of the directory. Continue? (y/n): ')
                if cont:
                    output_dir = enter_directory('Enter a directory: ', 'Error, invalid directory: ')
                    print()
                    extractor.filter_files(output_dir, FILE_FILTER)
                    print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))
                else:
                    print('Action cancelled.')

            elif choice == '5':  # Add dates to photos and videos in a folder (does not check sub-folders)
                cont = yes_no_input('This choice will rename the contents of the directory. Continue? (y/n): ')
                if cont:
                    output_dir = enter_directory('Enter a directory: ', 'Error, invalid directory: ')
                    print()
                    organizer.date_files(output_dir)
                    print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))
                else:
                    print('Action cancelled.')

            elif choice == '6':  # Sort files with dates added in the format: "YYYY-MM-DD_" (does not check sub-folders)
                cont = yes_no_input('This choice will reorder the contents of the directory. Continue? (y/n): ')
                if cont:
                    output_dir = enter_directory('Enter a directory: ', 'Error, invalid directory: ')
                    print()
                    organizer.sort_items(output_dir)
                    print('\nFinished. Output can be found at: ' + os.path.abspath(output_dir))
                else:
                    print('Action cancelled.')

            elif choice == '7':  # Exit program
                print('Exiting program...')
                exit()
            else:
                print('Error, invalid option: ' + str(choice))
        except AssertionError as e:
            print('\n\nError:', str(e))

        run = yes_no_input('\nRun again? (y/n): ')


if __name__ == '__main__':
    main()
