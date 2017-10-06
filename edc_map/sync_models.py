from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = ['edc_map.container', 'edc_map.innercontainer']
site_sync_models.register(sync_models, SyncModel)
