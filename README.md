# syncFolders

## 1. Argument Parsing
- The script starts by parsing command-line arguments using `argparse`. The arguments specify:
  - The **source** folder path (default is "source").
  - The **replica** folder path (default is "replica").
  - The **log file** path (default is "log.txt").
  - The **interval** in seconds between synchronization operations.

## 2. Logging Configuration
- Logging is set up to write information to the specified log file, providing timestamps and log levels (e.g., INFO).

## 3. File Comparison
- A function `compare_files` compares the content of two files using MD5 hash values. This helps determine if the files are identical or if the replica needs to be updated.

## 4. Folder Comparison and Synchronization
- The `compare_folders` function is the core of the script. It recursively compares the contents of the **source** and **replica** folders:
  - **Copying:** If a file or folder exists in the source but not in the replica, it is copied over.
  - **Updating:** If a file exists in both but the contents differ, the file in the replica is replaced with the one from the source.
  - **Deleting:** If a file or folder exists in the replica but not in the source, it is deleted from the replica.

## 5. Synchronization Process
- The `syncFolders` function handles the overall synchronization process:
  - It ensures the source and replica directories exist, creating the replica directory if necessary.
  - It repeatedly calls `compare_folders` at intervals specified by the user.
  - The function runs in a loop, continuously syncing the folders at the set interval.

## 6. Handling Termination
- The script includes handling for manual termination (via `KeyboardInterrupt`). When the user manually stops the script, it logs the termination and exits cleanly.

## Overall Functionality
The script keeps the **replica** folder in sync with the **source** folder by regularly checking and updating the contents based on file comparisons, ensuring that the replica is an accurate copy of the source over time.

 
