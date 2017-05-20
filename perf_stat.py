import asyncio
import pandas as pd
from komlogd.api import logging, session, crypto
from komlogd.api.transfer_methods import transfermethod
from komlogd.api.protocol.model.types import Datapoint, Datasource
from komlogd.api.protocol.model.schedules import CronSchedule

UARCH_DECODE_PATH_WIDE = 4 # Depends on your CPU microarchitecture. Haswell is 4

# Command to execute
PERF_CMD = "perf stat -a -- sleep 3 2>&1" # perf writes by default to stderr, we redirect it to stdout

# Uris to store command output in our data model
PERF_BASE_URI = 'tmp.commands.perf'

# perf ipc uri identified via web
PERF_IPC_URI = '.'.join((PERF_BASE_URI,'ipc'))

# uri to store the calculated cpu percentage, we nest it under PERF_BASE
PERF_CPU_TOTAL_URI = '.'.join((PERF_BASE_URI,'cpu_total'))


perf_ipc = Datapoint(uri=PERF_IPC_URI)
perf_cpu = Datapoint(uri=PERF_CPU_TOTAL_URI)

# Will execute every time ipc is received, and will set cpu_total
@transfermethod(p_in={'ipc':perf_ipc}, p_out={'cpu_total':perf_cpu})
def ipc_to_cpu(ts, ipc, cpu_total):
    cpu_total.data[ts]=ipc.data[ts]/UARCH_DECODE_PATH_WIDE*100


# a class to encapsulate a command execution data
# the stdout attribute it is mapped with a Datasource in our data model
class Command:
    def __init__(self, command, stdout):
        self.command = command
        self.stdout = Datasource(uri=stdout)

perf = Command(command=PERF_CMD, stdout=PERF_BASE_URI)

# transfer methods that periodically execute the command.
# The CronSchedule object is for executing it periodically, check
# komlogd documentation for more info about how to set the frecuency you want.
# by default is every minute (* * * * *).
@transfermethod(p_out={'cmd':perf}, schedule=CronSchedule())
async def run_cmd(ts, cmd):
    try:
        p = await asyncio.create_subprocess_shell(cmd.command, stdout=asyncio.subprocess.PIPE, stderr = asyncio.subprocess.PIPE)
        output = await p.stdout.read()
    except Exception as e:
        logging.logger.error('Exception running command.')
        logging.logger.error(str(e))
    else:
        await p.wait()
        content = output.decode('utf-8')
        cmd.stdout.data[ts] = content

