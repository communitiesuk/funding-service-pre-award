import contextlib
from operator import itemgetter

from marshmallow import post_dump
from marshmallow.fields import Method, String
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from fund_store.db.models.section import Section, SectionField


class SectionFieldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SectionField

    field_id = auto_field()
    display_order = auto_field()

    def get_display_type(self, obj):
        return obj.field.display_type

    def get_field_type(self, obj):
        return obj.field.field_type

    display_type = Method("get_display_type")
    field_type = Method("get_field_type")


class SectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    def get_form_name(self, obj):
        raise NotImplementedError

    def get_title(
        self,
        obj,
    ):
        raise NotImplementedError

    def get_weighting(self, obj):
        return obj.weighting if obj.weighting else None

    path = String()
    fields = Nested("SectionFieldSchema", many=True, allow_none=True)
    weighting = Method("get_weighting")


class LocalizedSectionSchema(SectionSchema):
    def get_form_name(self, obj, lang_code):
        with contextlib.suppress(ValueError):
            (form_name_container,) = obj.form_name
            return form_name_container.form_name_json[lang_code]

    def get_title(self, obj, lang_code):
        return obj.title_json.get(lang_code)

    def sort_children(self, data):
        if data.get("children"):
            sorted_children = sorted(data["children"], key=itemgetter("path"))
            data["children"] = sorted_children
        return data

    @post_dump
    def sort_children_post_dump(self, data, **kwargs):
        return self.sort_children(data)


class EnglishSectionSchema(LocalizedSectionSchema):
    def get_form_name(self, obj):
        return super().get_form_name(obj, "en")

    def get_title(self, obj):
        return super().get_title(obj, "en")

    children = Nested("EnglishSectionSchema", many=True, allow_none=True)
    form_name = Method("get_form_name")
    title = Method("get_title")


class WelshSectionSchema(LocalizedSectionSchema):
    def get_form_name(self, obj):
        return super().get_form_name(obj, "cy")

    def get_title(self, obj):
        return super().get_title(obj, "cy")

    children = Nested("WelshSectionSchema", many=True, allow_none=True)
    form_name = Method("get_form_name")
    title = Method("get_title")


SECTION_SCHEMA_MAP = {
    "en": EnglishSectionSchema,
    "cy": WelshSectionSchema,
}
