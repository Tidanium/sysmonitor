# todo integrate qt5 and flask into this
import asyncio
import os
import platform
import sys
import time

os.environ["TERM"] = "xterm-color" # catch-all for pseudo-error when env var TERM isn't set when using os.system('clear')
basepath = f"/{os.path.relpath('.', '/')}"
starttime = time.time()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        plat = platform.system().lower()
        if plat not in ['windows', 'darwin']:
            if sys.stdin.isatty():
                from bin.display.linux import terminalcurses as display
                #loop.run_until_complete(display.init(tty=True))
            else:
                from bin.display.linux import terminalcurses as display
                #loop.run_until_complete(display.init(tty=False))
        loop.run_until_complete(display.init())
    except (KeyboardInterrupt, SystemExit, SystemError, EOFError, TimeoutError):
        exit()
