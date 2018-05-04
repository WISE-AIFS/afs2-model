
from afs import config_handler


cfg = config_handler()
cfg.set_param('b', type='integer', required=True, default=10)
cfg.set_column('value')
cfg.summary()