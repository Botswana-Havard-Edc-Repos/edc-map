from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, weak=False, dispatch_uid="grep_google_map_image_on_post_save")
def grep_google_map_image_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        try:
            instance.store_image()
        except AttributeError as e:
            if 'store_image' not in str(e):
                pass
