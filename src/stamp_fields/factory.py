import factory

from config.splitted_settings.constants import (
    FIELDS_PER_GROUP,
    FIXTURES_LANGUAGE,
    SENTENCE_LEN,
)
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes

LOCALE = FIXTURES_LANGUAGE


class FieldsTypesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FieldsTypes

    name = factory.Faker("word", locale=LOCALE)
    help_text = factory.Faker("sentence", locale=LOCALE, nb_words=SENTENCE_LEN)

    class Params:
        """
        `bool` flag for re field.
        >>> f = FieldsTypesFactory.build(with_author=True)
        >>> f.re
        '(?s).*'
        """

        with_re = factory.Trait(re=r"(?s).*")


class GroupOfFieldsTypesFactory(factory.django.DjangoModelFactory):
    """Factory for `GroupOfFieldsTypes` objects.

    Will generate a fields if not passed.
    """

    class Meta:
        model = GroupOfFieldsTypes

    name = factory.Faker("word", locale=LOCALE)

    @factory.post_generation
    def fields(self, create, extracted, **kwargs) -> None:
        if not create:
            return
        if extracted:
            self.fields.set(extracted)
        elif not extracted:
            self.fields.set(FieldsTypesFactory.create_batch(FIELDS_PER_GROUP))
