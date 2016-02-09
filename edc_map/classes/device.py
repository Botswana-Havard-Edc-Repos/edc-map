from collections import namedtuple
# try:
#     from edc.device.device.classes import device
# except ImportError:
Device = namedtuple('Device', 'is_server')
device = Device('True')
