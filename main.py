import sys
# sys.path.append('.')
from service import supervisor
from tool import configTool
from tool import emailTool
from functools import partial

logDir = configTool.getConfig('genlog','log_dir')
logSuffix = configTool.getConfig('genlog','log_suffix')
threshold = {
    'cpu_temp_threshold' : configTool.getConfig('threshold','cpu_temp_threshold'),
    'gpu_temp_threshold': configTool.getConfig('threshold', 'gpu_temp_threshold'),
    'queue_list':configTool.getConfig('queue','queue_file')
}
sp = supervisor.supervisor('112.23.23.36', logDir, logSuffix, **threshold)
sp.dataMonitor()