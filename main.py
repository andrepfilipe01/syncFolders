
import hashlib
import os
import time
import shutil
import argparse
import logging

parser = argparse.ArgumentParser(description='Folder synchronization program')
parser.add_argument('--source', type=str, default="source", help='Source folder path')
parser.add_argument('--replica', type=str, default="replica", help='Replica folder path')
parser.add_argument('--log_file', type=str, default='log.txt', help='Log file path')
parser.add_argument('--interval', type=int, help='Time interval for synchronization in seconds')
args = parser.parse_args()

logging.basicConfig(filename=args.log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()


def compare_folders(source_f, replica_f):

    filesSource = os.listdir(source_f)
    filesReplica = os.listdir(replica_f)

    # Sync files from source to replica
    for file in filesSource:
        path_source = os.path.join(source_f, file)
        path_replica = os.path.join(replica_f, file)

        if os.path.isdir(path_source):
            if not os.path.exists(path_replica): # Check if directory exists in replica folder
                shutil.copytree(path_source, path_replica) # Copy directory tree from source to replica folder
                logging.info(f"Directory '{file}' has been copied.")
                print(f"Directory '{file}' has been copied.")
            else:
                compare_folders(path_source, path_replica) # Recursive call to compare subdirectories
        else:
            if file in filesReplica:
                if compare_files(path_source, path_replica): # Compare files in source and replica 
                    log_message = f"'{file}' is up to date."
                else:
                    os.remove(path_replica) # Remove file from replica
                    shutil.copy2(path_source, path_replica) # Copy file from source to replica if it has been updated
                    log_message = f"'{file}' has been updated."
            else:
                shutil.copy2(path_source, path_replica) # Copy file from source to replica if it doesn't exist in replica
                log_message = f"'{file}' has been copied."

            logging.info(log_message)
            print(log_message)

    # Remove files and directories from replica that are not in source
    for file in filesReplica:
        if file not in filesSource:
            path_replica = os.path.join(replica_f, file) # Get path of file in replica 
            if os.path.isdir(path_replica): # Check if file is a directory
                shutil.rmtree(path_replica) # Remove directory and its content
                log_message = f"Directory '{file}' has been deleted."
            else:
                os.remove(path_replica)
                log_message = f"'{file}' has been deleted."
            logging.info(log_message)
            print(log_message)

def syncFolders(source, replica, time_interval):
    
    if not os.path.isdir(source):
        raise argparse.ArgumentError(None, "The source folder doesn't exist.")
    
    if not os.path.isdir(replica):
        os.makedirs(replica)

    while True:
        try:
            compare_folders(source, replica) # Compare source and replica folders and synchronize them
            time.sleep(time_interval)
        except KeyboardInterrupt:
            logging.info("Program terminated manually!")
            raise SystemExit

if __name__ == '__main__':

    # Check if the log file exists, and create it if it doesn't
    if not os.path.exists(args.log_file):
        with open(args.log_file, 'w'):
            pass  # Create the file

    syncFolders(args.source, args.replica, args.interval)



