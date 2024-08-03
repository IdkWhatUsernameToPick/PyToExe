import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import sys
import shutil

def open_file_and_run_pyinstaller():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Prompt to select the Python file
    file_path = filedialog.askopenfilename(
        initialdir=current_dir,  # Set the initial directory
        filetypes=[("Python Files", "*.py")],
        title="Select a Python file"
    )
    
    if not file_path:
        print("No Python file selected. Exiting.")
        sys.exit(1)

    # Prompt to select the output directory
    output_dir = filedialog.askdirectory(
        initialdir=current_dir,
        title="Select an output directory"
    )
    
    if not output_dir:
        print("No output directory selected. Exiting.")
        sys.exit(1)

    print(f"Selected file: {file_path}")
    print(f"Selected output directory: {output_dir}")

    # Get the base name of the file (e.g., filename.py)
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]  # Remove the .py extension

    # Define the paths for spec file, build folder, and dist folder
    spec_file = os.path.join(output_dir, f"{base_name}.spec")
    build_folder = os.path.join(output_dir, "build")
    dist_folder = os.path.join(output_dir, "dist")
    
    # Build the pyinstaller command
    pyinstaller_command = ["pyinstaller", "--onefile", file_path, "--distpath", dist_folder, "--workpath", build_folder, "--specpath", output_dir]
    
    # Run the pyinstaller command
    try:
        subprocess.run(pyinstaller_command, check=True)
        print(f"Successfully ran pyinstaller on {file_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error running pyinstaller: {e}")
        sys.exit(1)  # Exit with error code

    # Remove the .spec file if it exists
    if os.path.isfile(spec_file):
        os.remove(spec_file)
        print(f"Removed {spec_file}")

    # Remove the build folder if it exists
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder)
        print(f"Removed {build_folder}")

    # Paths for .exe file and destination
    exe_file = os.path.join(dist_folder, f"{base_name}.exe")
    destination = os.path.join(output_dir, f"{base_name}.exe")
    
    # Check if dist folder exists and the .exe file is present
    if os.path.isdir(dist_folder) and os.path.isfile(exe_file):
        shutil.copy(exe_file, destination)
        print(f"Copied {exe_file} to {destination}")

        # Verify that the file was copied successfully
        if os.path.isfile(destination):
            # Remove the dist folder
            shutil.rmtree(dist_folder)
            print(f"Removed {dist_folder}")
        else:
            print("Error: The copied .exe file is not found in the output directory")
            sys.exit(1)  # Exit with error code if .exe file is not found after copying
    else:
        print("Error: .exe file not found in the dist folder")
        sys.exit(1)  # Exit with error code if .exe file is not found

    # Exit the script successfully
    sys.exit(0)  # Exit with success code

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open the file dialog and run pyinstaller
open_file_and_run_pyinstaller()

# The script will exit before reaching here, so no need to start the Tkinter event loop
