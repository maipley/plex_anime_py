import os, argparse

movies_path = '/plex/anime/movies'
simple = False

def spacer(): print("----------------------------------------")


def movie_fix(simple):
    all_movies_good = True
    for folder in sorted(os.listdir(movies_path)):
        movie_folder = os.path.join(movies_path, folder)
        if os.path.isdir(movie_folder):
            for file in sorted(os.listdir(movie_folder)):
                file_wo_ext = os.path.splitext(file)[0]
                if file_wo_ext == folder:
                    if simple == False:
                        print(f"{file} is already named correctly")
                        spacer()
                        continue
                    else:
                        continue
                print(folder)
                if file.endswith('.mp4'):
                    old_name = file
                    os.rename(os.path.join(movies_path, folder, file), os.path.join(movies_path, folder, f'{folder}.mp4'))
                    print(f"-> {old_name} was renamed to {folder}.mp4")
                    all_movies_good = False
                    break
                elif file.endswith('.mkv'):
                    old_name = file
                    os.rename(os.path.join(movies_path, folder, file), os.path.join(movies_path, folder, f'{folder}.mkv'))
                    print(f"-> {old_name} was renamed to {folder}.mkv")
                    all_movies_good = False
                    break
                spacer()
    if all_movies_good == True:
        print("All movies were already named correctly")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Selects the mode")
    parser.add_argument('-s', '--simple', action='store_true', help='Simple mode')
    args = parser.parse_args()
    movie_fix(simple = args.simple)
