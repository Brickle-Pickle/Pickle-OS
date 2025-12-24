# rm.py -> Remove files or directories
import uos
from system.config import BIG_DISPLAY
from system.shared_states import input_buffer

def rm(args):
    if len(args) == 0:
        BIG_DISPLAY.set_text_size(1)
        BIG_DISPLAY.show_error("Error:", "Usage: rm <file>")
        return
    
    files = []
    folders = []
    force_delete_folders = False

    for arg in args:
        if arg.startswith("/"):
            folders.append(arg[1:])
        else:
            if "-" not in arg:
                if "." in arg:
                    result = get_files(arg)
                    if isinstance(result, list):
                        files.extend(result)
                    else:
                        files.append(result)
                else:
                    if arg != "*":
                        folders.append(arg)
                    else:
                        all_items = get_all_files()
                        path = input_buffer["actual_path"]
                        for item in all_items:
                            full_path = path + "/" + item if path != "/" else "/" + item
                            try:
                                # 0x4000 is the bit for a directory
                                if uos.stat(full_path)[0] & 0x4000:
                                    folders.append(item)
                                else:
                                    files.append(item)
                            except OSError:
                                # If stat fails, assume it is a file
                                files.append(item)
            else:
                if arg == "-f":
                    force_delete_folders = True

    delete_files(files)
    if force_delete_folders:
        delete_folders(folders)
    
    BIG_DISPLAY.show_error(["Success: files and", "folders deleted."])
    BIG_DISPLAY.clear()
    BIG_DISPLAY.show()
    input_buffer["reset_keyboard"] = True
    input_buffer["reset_shell"] = True

def get_files(arg):
    if "*" not in arg:
        return arg
    else:
        if len(arg) == 1:
            return get_all_files()
        elif arg.startswith("*"):
           return get_all_files_endswith(arg[1:])
        else:
           return get_all_files_startswith(arg[1:])

def get_all_files():
    path = input_buffer["actual_path"]
    selected_files = uos.listdir(path)
    return selected_files

def get_all_files_endswith(endswith):
    path = input_buffer["actual_path"]
    selected_files = uos.listdir(path)
    return [file for file in selected_files if file.endswith(endswith)]

def get_all_files_startswith(startswith):
    path = input_buffer["actual_path"]
    selected_files = uos.listdir(path)
    return [file for file in selected_files if file.startswith(startswith)]

def rmtree(path):
    try:
        for entry in uos.listdir(path):
            entry_path = path + "/" + entry
            # 0x4000 is the bit for a directory
            if uos.stat(entry_path)[0] & 0x4000:
                rmtree(entry_path)
            else:
                uos.remove(entry_path)
        uos.rmdir(path)
    except OSError:
        pass

def delete_files(files):
    path = input_buffer["actual_path"]
    for file in files:
        full_path = path + "/" + file if path != "/" else "/" + file
        try:
            uos.remove(full_path)
        except OSError:
            pass

def delete_folders(folders):
    path = input_buffer["actual_path"]
    for folder in folders:
        full_path = path + "/" + folder if path != "/" else "/" + folder
        rmtree(full_path)