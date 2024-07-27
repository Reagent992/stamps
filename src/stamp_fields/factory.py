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


class GroupOfFieldsTypesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupOfFieldsTypes

    name = factory.Faker("word", locale=LOCALE)

    @factory.post_generation
    def fields(self, create, extracted, **kwargs) -> None:
        if not create:
            return
        if not extracted:
            extracted = FieldsTypesFactory.create_batch(FIELDS_PER_GROUP)
        self.fields.add(*extracted)
