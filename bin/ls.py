# ls.py -> List directory contents.
import uos

def ls():
    uos.listdir()
    for file in uos.listdir():
        print(file.ljust(20), end="")
