from django.core.management.base import BaseCommand, CommandError

from mainapp.models import Stamp, StampGroup
from printy.models import Printy, PrintyGroup
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes


class Command(BaseCommand):
    help = "Delete all stamps printys stamp fields."

    def handle(self, *args, **options):
        try:
            Printy.objects.all().delete()
            PrintyGroup.objects.all().delete()
            Stamp.objects.all().delete()
            StampGroup.objects.all().delete()
            FieldsTypes.objects.all().delete()
            GroupOfFieldsTypes.objects.all().delete()

        except Exception as e:
            raise CommandError(e)
