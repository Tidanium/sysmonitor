import datetime
import time

import psutil

from main import starttime

_cpu = {
	"30s": [],
	"5m": [],
	"15m": []
}
async def avg(l):
	s = sum(l)
	l = len(l)
	if s in [0, 0.0]:
		return 0.0
	return s/l

async def percent(percpu:bool=False):
	pcnt = psutil.cpu_percent(percpu=percpu)
	return pcnt

async def uptime(boot:bool=True):
	upt = time.time() - starttime
	if boot:
		upt = str(datetime.timedelta(seconds=int(datetime.datetime.now().timestamp() - psutil.boot_time())))
	return upt

async def processes():
	"""
	Dict:
	{
		'pid': pid,
		'name': name,
		'parent': parent,
		'children': children,
		'username': username,
		'status': status,
		'terminal': terminal,
		'nice': nice,
		'ionice': ionice,
		'threads': threads,
		'cpu_times': cpu_times,
		'cpu_percent': cpu_percent,
		'cpu_num': cpu_num,
		'memory_percent': memory_percent,
		'open_files': open_files,
		'connections': connections
	}
	:returns dict:
	"""
	pidtarget = None
	for proc in psutil.process_iter():
		try:
			pid = proc.pid
		except psutil.NoSuchProcess:
			pass
		else:
			pidtarget = pid
	if pidtarget is not None:
		target = psutil.Process(pid=pidtarget)
		cpu = target.as_dict(attrs=['pid', 'name', 'parent', 'children', 'username', 'status', 'terminal', 'nice',
		                            'ionice', 'threads', 'cpu_times', 'cpu_percent', 'cpu_num', 'memory_percent',
		                            'open_files', 'connections'])
	return cpu
