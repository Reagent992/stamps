import factory

from config.splitted_settings.constants import (
    FIXTURES_LANGUAGE,
    GROUP_COLOR,
    IMAGE_FORMAT,
    IMAGE_WIDTH,
    ITEM_COLOR,
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
        color=GROUP_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    published = True


class PrintyFactory(factory.django.DjangoModelFactory):
    """Factory for generating Printy objects.

    By default, it generates a new PrintyGroup for each Printy. You can pass
    an existing PrintyGroup to attach the Printy to it.
    """

    class Meta:
        model = Printy

    title = factory.Faker("sentence", nb_words=SENTENCE_LEN, locale=LOCALE)
    image = factory.django.ImageField(
        color=ITEM_COLOR, width=IMAGE_WIDTH, image_format=IMAGE_FORMAT
    )
    description = factory.Faker("paragraph", locale=LOCALE)
    price = factory.Faker("random_int", min=MIX_PRICE, max=MAX_PRICE)
    published = True
    group = factory.SubFactory(PrintyGroupFactory)
