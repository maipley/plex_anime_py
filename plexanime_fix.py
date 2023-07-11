import os, shutil
from plexanime_movie import movie_fix
movies_path = '/plex/anime/movies'
series_path = '/plex/anime/series'
is_movie = False
is_series = False
# ftf -> folder to fix

def series_fix():
    for f in os.listdir(end_path):
        if f.endswith('.mp4'):
            os.rename(os.path.join(end_path, f), os.path.join(end_path, 'E01.mp4'))
            print(f"-> {f} was renamed to {ftf}.mp4")
        elif f.endswith('.mkv'):
            os.rename(os.path.join(end_path, f), os.path.join(end_path, 'E01.mkv'))
            print(f"-> {f} was renamed to {ftf}.mkv")

while True:
    chosen_dir = input('Where is the wrong folder? (m/s): ')
    if chosen_dir == 'm':
        directory = movies_path
        break
    elif chosen_dir == 's':
        directory = series_path
        break
    else:
        print('Please enter a valid option.')
folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
print('Select a folder to fix: ')
for i, folder in enumerate(folders):
    print(f'{i+1}: {folder}')
while True:
    ftf_num = int(input('Enter the number of the folder to fix: '))
    if 1 <= ftf_num <= len(folders):
        ftf = folders[ftf_num-1]
        print(f'You chose {ftf}')
        break
    else:
        print(f"Please enter a number between 1 and {len(folders)}")

if chosen_dir == 'm':
    dst_dir = series_path
    is_series = True
    print(f"{ftf} will be moved to series.")
elif chosen_dir == 's':
    dst_dir = movies_path
    is_movie = True
    print(f"{ftf} will be moved to movies.")

initial_path = os.path.join(directory, ftf)
end_path = os.path.join(dst_dir, ftf)

while True:
    confirm = input("Are you sure you want to move this folder? (y/n): ")
    if confirm == 'y' or confirm == '':
        shutil.move(initial_path, end_path)
        print(f"{ftf} has been moved.")
        if is_movie:
            movie_fix(simple=True)
        if is_series:
            series_fix()
        exit()
    elif confirm == 'n':
        print("Aborting...")
        exit()
    else:
        print("Please enter a valid option.")
