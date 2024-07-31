from django.core.management.base import BaseCommand, CommandError

from mainapp.factory import StampFactory, StampGroupFactory
from printy.factory import PrintyFactory, PrintyGroupFactory
from stamp_fields.factory import FieldsTypesFactory, GroupOfFieldsTypesFactory


class Command(BaseCommand):
    help = "Generate (20 * multiplier) stamps."

    def add_arguments(self, parser):
        parser.add_argument("multiplier", type=int)

    def handle(self, *args, **options):
        amount = 20 * options.get("multiplier", 1)
        try:
            FieldsTypesFactory.create_batch(amount)
            GroupOfFieldsTypesFactory.create_batch(amount // 4)
            PrintyGroupFactory.create_batch(amount // 4)
            PrintyFactory.create_batch(amount)
            StampGroupFactory.create_batch(amount // 4)
            StampFactory.create_batch(amount)
        except Exception as e:
            raise CommandError(e)
