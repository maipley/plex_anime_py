import os, shutil, argparse
from plexanime_movie import movie_fix
from wait_keypress import wait_for_keypress
from moviepy.video.io.VideoFileClip import VideoFileClip

# Paths
src_path = "/home/anime/anime"
movies_path = "/plex/anime/movies"
series_path = "/plex/anime/series"
ext = ".mp4", ".mkv"
is_movie = False

# Parse arguments
parser = argparse.ArgumentParser(description="Selects the mode")

group = parser.add_mutually_exclusive_group()

group.add_argument('-a', '--auto', action='store_true', help='Automatic mode')
group.add_argument('-m', '--manual', action='store_true', help='Manual mode')

args = parser.parse_args()

# Assign the mode values
if args.auto:
    mode = 1
    print("Mode: Automatic")
elif args.manual:
    mode = 2
    print("Mode: Manual")
else:
    mode = 0
    print("Mode: Normal")
# Functions
def list_folders(path):
    for sf_name in sorted(os.listdir(path)):
        print(sf_name)

def is_folder_empty(folder):
    return len(os.listdir(folder)) == 0

# Main loop
for folder_name in sorted(os.listdir(src_path)):
    folder = os.path.join(src_path, folder_name)
    duration = -1
    if os.path.isdir(folder):
        # Check if the folder is empty
        if mode <= 1 and is_folder_empty(folder):
            shutil.rmtree(folder)
            print(f"{folder_name} was empty and was deleted")
            continue
        # Waits until keypress and then clears the screen
        if mode == 0 or mode == 2:
            wait_for_keypress(f"Press any key to continue...")
            os.system('clear')
        # Manual type selection
        if mode == 2:
            if is_folder_empty(folder):
                print(f"It seems that {folder_name} is empty")
                while True:
                    dlete = input("Do you want to delete it? (y/n): ")
                    type.replace(" ", "")
                    if dlete == 'y' or dlete == '':
                        shutil.rmtree(folder)
                        print(f"{folder_name} was deleted")
                        break
                    elif dlete == 'n':
                        folder = os.path.join(src_path, f",{folder_name}")
                        continue
            while True:
                type = input(f"Is {folder_name} a movie or a series? (m/s): ")
                type.replace(" ", "")
                if type == 'm' or type == 's':
                    break
                elif type == 'z':
                    folder = os.path.join(src_path, f",{folder_name}")
                    print(f"{folder_name} skipped")
                    continue
                else:
                    print("Invalid input")
        # Automatic type selection
        elif mode <= 1:
            # Get the duration of the first .mkv file
            print(f"Checking {folder_name}")
            for file in sorted(os.listdir(folder)):
                if file.endswith(ext):
                    clip = VideoFileClip(os.path.join(folder, file))
                    duration = clip.duration
                    clip.reader.close()
                    clip.audio.reader.close_proc()
                    break
        # Automatic assignment of the destination folder
        if mode == 1:
            if duration >= 2700:
                dst_folder = os.path.join(movies_path, folder_name)
                print(f"{folder_name} is a movie folder")
                is_movie = True
            else:
                dst_folder = os.path.join(series_path, folder_name)
                print(f"{folder_name} is a series folder")
        # Manual/Normal assignment of the destination folder
        elif mode == 2 or mode == 0:
            while True:
                answer = input(f"Do you want to change the name of the folder {folder_name}? (y/n): ")
                answer.replace(" ", "")
                if answer == 'n' or  answer == '':
                    name_change = 0
                    break
                elif answer == 'y':
                    name_change = 1
                    break
                elif answer == 'z':
                    os.rename(folder ,os.path.join(src_path, f",{folder_name}"))
                    print(f"{folder_name} skipped")
                    name_change = -1
                    break
                else:
                    print("Invalid input")
            # New name for the folder
            if name_change == -1:
                continue
            elif name_change == 1:
                # List all the subfolders
                print('')
                print('[MOVIES]')
                list_folders(movies_path)
                print('')
                print('[SERIES]')
                list_folders(series_path)
                while True:
                    new_name = input("New name: ")
                    new_name.replace(" ", "")
                    if new_name == '':
                        print("Please enter a valid name")
                    else:
                        break
            else:
                new_name = folder_name
            # Check if the folder is a movie or a series
            if type == 'm' or duration >= 2700:
                dst_folder = os.path.join(movies_path, new_name)
                print(f"{new_name} is a movie folder")
                is_movie = True
            elif type == 's' or duration < 2700:
                dst_folder = os.path.join(series_path, new_name)
                print(f"{new_name} is a series folder")
                while True:
                    season = input("What season is it?: ")
                    season.replace(' ', '')
                    if season == '':
                        season = 1
                    season = int(season)
                    if 0 <= season <= 25:
                        break
                    else:
                        print("Invalid input, please valid season number (0 and up)")
                dst_folder = os.path.join(dst_folder, f"Season {season}")
        # Check if the destination folder exists
        os.makedirs(dst_folder, exist_ok=True)
        # Move all the .mkv or .mp4 files from the current subfolder to the new folder
        for file in sorted(os.listdir(folder)):
            if file.endswith(ext):
                shutil.move(os.path.join(folder, file), dst_folder)
                print(f"{file} moved")

# Iterate over all the subfolders inside the source folder
for subfolder_name in sorted(os.listdir(src_path)):
    if subfolder_name.startswith("+"):
        continue
    if subfolder_name.startswith(","):
        subfolder_name = subfolder_name[1:]
        continue
    subfolder = os.path.join(src_path, subfolder_name)
    if os.path.isdir(subfolder):
        # delete the folder
        shutil.rmtree(subfolder)
        print(f"{subfolder_name} deleted")
print("There is no more folders")

# Rename movies
if is_movie:
    print("Renaming movies")
    movie_fix(simple = True)
    print("Done")
