import psutil


async def virtual():
    return psutil.virtual_memory()

async def swap():
    return psutil.swap_memory()
