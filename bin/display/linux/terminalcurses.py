import asyncio
import curses

from bin import settings, misc
from bin.montools import cpu, memory

# start cursor app
stdscr = curses.initscr()
curses.start_color()

async def init():
    cpu_count = settings.CPU.count()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    while True:
        try:
            cpu_p       = await cpu.percent()
            cpu_pc      = await cpu.percent(True)
            uptime      = await cpu.uptime()
            vmem        = await memory.virtual()
            smem        = await memory.swap()
            fmt         =  f'─╴'; stdscr.addstr(fmt)
            fmt         =  f'Uptime'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         =  f': {uptime}\n\n'; stdscr.addstr(fmt)
            fmt         =  f'┬╴'; stdscr.addstr(fmt)
            fmt         =  f'CPU'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         =  f' {cpu_p}%\n'; stdscr.addstr(fmt)
            fmt         =   ''
            for i in range(cpu_count):
                if i != cpu_count-1:
                    fmt += f'├──╴{i+1} {cpu_pc[i]}%\n'
                else:
                    fmt += f'╰──╴{i+1} {cpu_pc[i]}%\n'
            vmem_total = misc.convert_size(vmem.total); vmem_avail = misc.convert_size(vmem.available); vmem_used = misc.convert_size(vmem.used); smem_total = misc.convert_size(smem.total>>10); smem_used = misc.convert_size(smem.used>>10); smem_free = misc.convert_size(smem.free>>10)
            fmt         +=  '\n'; stdscr.addstr(fmt)
            fmt         =  f'┬╴'; stdscr.addstr(fmt)
            fmt         =  f'Memory\n'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         = (f'├┬╴Virtual\n'
                           f'│├──────╴Total: {vmem_total}\n'
                           f'│├──╴Available: {vmem_avail}\n'
                           f'│╰───────╴Used: {vmem_used}\n'
                           f'╰┬╴Swap\n'
                           f' ├──────╴Total: {smem_total}\n'
                           f' ├──╴Available: {smem_free}\n'
                           f' ╰───────╴Used: {smem_used}')
            stdscr.addstr(fmt)
            stdscr.refresh(); stdscr.clear()
            await asyncio.sleep(settings.Output.interval)
        except Exception as e:
            #endsession(e.with_traceback(e))
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            print('\n',e.with_traceback(e))
            break

async def updatescr(scr=stdscr):
    return scr.refresh()

# end cursor app
def endsession(e=None):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return print(e) if e else None
