#%%
# Möf Selvi

import time
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller

virtualkb = Controller()
working = False
canceled = False
sleeptime = 0.01


def on_activate_t():
    cb_str_orig = pyperclip.paste()
    cb_str = cb_str_orig.replace("\r","").strip()+"\n"
    cb_str = cb_str.replace("\n","\t\n")
    pyperclip.copy(cb_str)
    print("A new empty column added to the clipboard")

def on_activate_v():
    global working, canceled, sleeptime

    if working:
        return
    
    virtualkb.release(Key.ctrl_l)
    virtualkb.release(Key.alt_l)
    virtualkb.release('v')

    print('Pasting the table into the form...')
    cb_str_orig = pyperclip.paste()
    # pyperclip.copy(s)

    cb_str = cb_str_orig.replace("\r","").strip()
    print("CB:",cb_str)

    if "\t" in cb_str or "\n" in cb_str:
        values = cb_str.replace("\n","\t").split("\t")
        print(values)
        working = True
        for v in values:

            if canceled:
                break

            pyperclip.copy(str(v))
            # print(pyperclip.paste())
            
            virtualkb.press(Key.ctrl_l)
            time.sleep(sleeptime)

            virtualkb.press('a')
            virtualkb.release('a')

            time.sleep(sleeptime)

            virtualkb.press('v')
            virtualkb.release('v')

            time.sleep(sleeptime)

            virtualkb.release(Key.ctrl_l)
            time.sleep(sleeptime)
            virtualkb.press(Key.tab)
            virtualkb.release(Key.tab)
            time.sleep(sleeptime)


        virtualkb.press(Key.tab)
        virtualkb.release(Key.tab)
        virtualkb.press(Key.tab)
        virtualkb.release(Key.tab)
        virtualkb.press(Key.tab)
        virtualkb.release(Key.tab)

        pyperclip.copy(cb_str_orig)
        time.sleep(1)
        working=False
        print("Pasted all values.")
    else:
        print("No table found on the clipboard. Copy some cells.")



def on_activate_quit():
    print('Stopped.')
    canceled = True
    h.stop()

print("# The program has started. Press ctrl+alt+x to quit. #")

with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+t': on_activate_t,
        '<ctrl>+<alt>+v': on_activate_v,
        '<ctrl>+<alt>+x': on_activate_quit}) as h:
    h.join()

