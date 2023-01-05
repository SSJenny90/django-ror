from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import Organization


@receiver(post_save, sender=Organization)
def save_registered_domains(sender, instance, created, **kwargs):
    updated = kwargs['update_fields']
