import shutil

# specify the folder path
folder_to_zip = 'simulation_data'

# create a Zip file of the folder and its subfolders recursively
shutil.make_archive('simulation_data', 'zip', folder_to_zip)

print('Folder zipped successfully!')
