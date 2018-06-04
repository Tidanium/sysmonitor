import asyncio
import os

from bin import settings
from bin.montools import cpu


async def init(tty:bool):
	if tty:
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			cpu_p    =  await cpu.percent()
			#cpu_load = await cpu.avgload()
			uptime   = await cpu.uptime()
			fmt  =  f">>> Uptime: {uptime} seconds\n"
			fmt += ( ">>> CPU\n"
			        f"\tTOTAL\t{cpu_p}%")
			#if cpu_load[0] is not None:
			#	fmt += f"\t30s: {cpu_load[0]}%"
			#if cpu_load[1] is not None:
			#	fmt += f"\t5m:  {cpu_load[1]}%"
			#if cpu_load[2] is not None:
			#	fmt += f"\t15m: {cpu_load[2]}%"
			fmt += "\n"
			cpu_p =  await cpu.percent(percpu=True)
			fmt += (f"\tCPU 1\t{cpu_p[0]}%\n" # todo make this change in length based on number of cpu's in computer
			        f"\tCPU 2\t{cpu_p[1]}%\n"
			        f"\tCPU 3\t{cpu_p[2]}%\n"
			        f"\tCPU 4\t{cpu_p[3]}%\n")
			print(fmt)
			await asyncio.sleep(settings.Output.interval)

