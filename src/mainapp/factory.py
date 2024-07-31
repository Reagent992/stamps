import factory

from config.splitted_settings.constants import (
    FIXTURES_LANGUAGE,
    GROUP_COLOR,
    IMAGE_FORMAT,
    IMAGE_WIDTH,
    ITEM_COLOR,
    MAX_PRICE,
    MIX_PRICE,
    PRINTY_PER_STAMP,
    SENTENCE_LEN,
)
from mainapp.models import Stamp, StampGroup
from printy.models import Printy
from stamp_fields.models import GroupOfFieldsTypes

LOCALE = FIXTURES_LANGUAGE


class StampGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StampGroup

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    image = factory.django.ImageField(
        color=GROUP_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    published = True


class StampFactory(factory.django.DjangoModelFactory):
    """Factory for Stamp objects.
    It is required that:
        - StampGroups already exists.
        - Printy already exists.
        - GroupOfFieldsTypes already exists.
    """

    class Meta:
        model = Stamp

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    image = factory.django.ImageField(
        color=ITEM_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    description = factory.Faker("paragraph", locale=LOCALE)
    price = factory.Faker("random_int", min=MIX_PRICE, max=MAX_PRICE)
    published = True
    form_fields = factory.Iterator(GroupOfFieldsTypes.objects.all())
    group = factory.Iterator(StampGroup.objects.all())

    @factory.post_generation
    def printy(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            self.printy.set(Printy.objects.order_by("?")[:PRINTY_PER_STAMP])
