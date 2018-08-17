from afs import config_handler

cfg = config_handler()
cfg.set_param('b', type='string', required=False)
cfg.set_features(True)
cfg.set_column('a')
cfg.summary()