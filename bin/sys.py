# sys.py - Monitoring cpu, memory and disk usage
import machine
import gc
import uos
from system.shared_states import input_buffer
from system.config import BIG_DISPLAY

def sys(args):
    _cpu = True if "-cpu" in args else False
    _mem = True if "-mem" in args else False
    _disk = True if "-dsk" in args  or "-disk" in args else False

    if not _cpu and not _mem and not _disk:
        BIG_DISPLAY.show_error(["Usage error:", "no options"])
        input_buffer["errased"] = True
        input_buffer["reset_keyboard"] = True
        input_buffer["reset_shell"] = True
        return

    messages = []

    if _cpu:
        messages.append("CPU: {:04}MHz".format(machine.freq() // 1000000)) # Only show MHz (max 4 digits)
    if _mem:
        messages.append("MEM: {:04}KB".format(gc.mem_free() // 1024)) # Only show KB (max 4 digits)
    if _disk:
        stat = uos.statvfs("/")
        messages.append("DISK: {:02}%".format((stat[3] * 100) // stat[2])) # Only show % (max 2 digits)

    BIG_DISPLAY.show_error(messages)
    
    input_buffer["errased"] = True
    input_buffer["reset_keyboard"] = True
    input_buffer["reset_shell"] = True