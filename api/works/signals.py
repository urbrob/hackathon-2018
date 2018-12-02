from django.db.models.signals import post_save
from django.dispatch import receiver
from works.models import Report
from works.tasks import start_tests


@receiver(post_save, sender=Report)
def start_report(sender, instance, created, **kwargs):
    if created:
        start_tests(instance)
