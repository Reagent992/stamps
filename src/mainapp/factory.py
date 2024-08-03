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
from printy.factory import PrintyFactory
from stamp_fields.factory import GroupOfFieldsTypesFactory

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

    Fields: form_fields, group and printy will be generated if not passed.
    """

    class Meta:
        model = Stamp

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    description = factory.Faker("paragraph", locale=LOCALE)
    price = factory.Faker("random_int", min=MIX_PRICE, max=MAX_PRICE)
    published = True
    image = factory.django.ImageField(
        color=ITEM_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    form_fields = factory.SubFactory(GroupOfFieldsTypesFactory)
    group = factory.SubFactory(StampGroupFactory)

    @factory.post_generation
    def printy(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.printy.set(extracted)
        if not extracted:
            self.printy.set(PrintyFactory.create_batch(PRINTY_PER_STAMP))
