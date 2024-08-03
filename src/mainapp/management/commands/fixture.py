import random

from django.core.management.base import BaseCommand, CommandError

from mainapp.factory import StampFactory, StampGroupFactory
from printy.factory import PrintyFactory, PrintyGroupFactory
from stamp_fields.factory import GroupOfFieldsTypesFactory


class Command(BaseCommand):
    help = "Generate (20 * <input_int>) stamps."

    def add_arguments(self, parser):
        parser.add_argument("multiplier", type=int)

    def handle(self, *args, **options):
        amount = 20 * options.get("multiplier", 1)
        try:
            stamp_fields_group = GroupOfFieldsTypesFactory.create_batch(
                amount // 4
                )
            printy_groups = PrintyGroupFactory.create_batch(amount // 4)
            printys = [
                PrintyFactory(
                    group=random.choice(printy_groups)
                    ) for _ in range(amount)
                ]
            groups = StampGroupFactory.create_batch(amount // 4)
            for stamp_fields, stamp_group in zip(stamp_fields_group, groups):
                for _ in range(amount // 4):
                    StampFactory.create(
                        group=stamp_group,
                        form_fields=stamp_fields,
                        printy=random.sample(printys, amount // 4),
                    )

        except Exception as e:
            raise CommandError(e)
