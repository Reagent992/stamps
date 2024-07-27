import factory

from config.splitted_settings.constants import (
    FIXTURES_LANGUAGE,
    IMAGE_COLOR,
    IMAGE_FORMAT,
    IMAGE_WIDTH,
    MAX_PRICE,
    MIX_PRICE,
    SENTENCE_LEN,
)
from printy.models import Printy, PrintyGroup

LOCALE = FIXTURES_LANGUAGE


class PrintyGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrintyGroup

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    image = factory.django.ImageField(
        color=IMAGE_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    published = True


class PrintyFactory(factory.django.DjangoModelFactory):
    """Factory for Printy objects.
    It is required that PrintyGroups already exists."""

    class Meta:
        model = Printy

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    image = factory.django.ImageField(
        color=IMAGE_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    description = factory.Faker("paragraph", locale=LOCALE)
    price = factory.Faker("random_int", min=MIX_PRICE, max=MAX_PRICE)
    published = True
    group = factory.Iterator(PrintyGroup.objects.all())
