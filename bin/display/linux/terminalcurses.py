import asyncio
import curses

from bin import settings, misc
from bin.montools import cpu, memory


async def init():
    stdscr = curses.initscr()
    curses.start_color()
    cpu_count = settings.CPU.count() # as no computer has plug n' play cpu's, keep it static upon init
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    c = 0 # c = refresh count. used for debugging
    while True:
        try:
            cpu_p       = await cpu.percent()
            cpu_pc      = await cpu.percent(True)
            uptime      = await cpu.uptime()
            vmem        = await memory.virtual()
            smem        = await memory.swap()
            fmt         =  f'─╴'; stdscr.addstr(fmt)
            fmt         =  f'Uptime'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         =  f': {uptime}\n{c} frames\n'; stdscr.addstr(fmt)
            fmt         =  f'┬╴'; stdscr.addstr(fmt)
            fmt         =  f'CPU'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         =  f' {cpu_p}%\t.\n'; stdscr.addstr(fmt)
            fmt         =  f''
            for i in range(cpu_count):
                if i != cpu_count-1:
                    fmt += f'├──╴{i+1} {cpu_pc[i]}%\t.\n'
                else:
                    fmt += f'╰──╴{i+1} {cpu_pc[i]}%\t.\n'
            vmem_total  = misc.convert_size(vmem.total)
            vmem_avail  = misc.convert_size(vmem.available)
            vmem_used_  = misc.convert_size(vmem.total - vmem.available)
            vmem_pcnt_u = misc.fmt_percent(vmem.percent)
            vmem_pcnt_a = misc.fmt_percent(vmem.percent, invert=True)
            smem_total  = misc.convert_size(smem.total>>10)
            smem_used_  = misc.convert_size(smem.used>>7)
            smem_avail  = misc.convert_size(smem.free>>10)
#           todo fix values showing as None. cause unknown. idea: have the memory written to a file each refresh to further gain knowledge of the values
#            if smem_used_ is None: # patching of value being displayed as None - rare occurrence; 7 of 130 times.
#                smem_used_ = '0 B'
#            if smem_avail is None:
#                smem_avail = smem_total
            smem_pcnt_u = misc.fmt_percent(smem.percent)
            smem_pcnt_a = misc.fmt_percent(smem.percent, invert=True)
            fmt         +=  '\n'; stdscr.addstr(fmt)
            fmt         =  f'┬╴'; stdscr.addstr(fmt)
            fmt         =  f'Memory\n'; stdscr.addstr(fmt, curses.color_pair(1))
            fmt         = (f'├┬╴Virtual\n'
                           f'│├──────╴Total: {vmem_total}\n'
                           f'│├──╴Available: {vmem_avail}  {vmem_pcnt_a}\n'
                           f'│╰───────╴Used: {vmem_used_}  {vmem_pcnt_u}\n'
                           f'╰┬╴Swap\n'
                           f' ├──────╴Total: {smem_total}\n'
                           f' ├──╴Available: {smem_avail}  {smem_pcnt_a}\n'
                           f' ╰───────╴Used: {smem_used_}  {smem_pcnt_u}')
            stdscr.addstr(fmt)
            stdscr.refresh(); stdscr.clear()
            await asyncio.sleep(settings.Output.interval)
            c += 1
        except Exception as e:
            #endsession(e.with_traceback(e))
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
            print('\n',e.with_traceback(e))
            break

# end cursor app
def endsession(e=None):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return print(e) if e else None
