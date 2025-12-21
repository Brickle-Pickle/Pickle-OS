# shared_states.py -> Shared states for the MiniPC between threads.
input_buffer = {
    "enter": False,
    "input": "",
    "lock": False,
}