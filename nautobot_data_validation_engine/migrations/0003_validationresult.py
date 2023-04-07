# Generated by Django 3.2.18 on 2023-04-07 19:39

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.extras.models.mixins
import taggit.managers
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0057_jobbutton"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("nautobot_data_validation_engine", "0002_required_unique_types_regex_context"),
    ]

    operations = [
        migrations.CreateModel(
            name="ValidationResult",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("class_name", models.CharField(max_length=100)),
                ("method_name", models.CharField(max_length=100)),
                ("last_validation_date", models.DateField()),
                ("object_id", models.CharField(max_length=200)),
                ("validated_attribute", models.CharField(blank=True, max_length=100, null=True)),
                ("validated_attribute_value", models.CharField(blank=True, max_length=100, null=True)),
                ("expected_attribute_value", models.CharField(blank=True, max_length=100, null=True)),
                ("valid", models.BooleanField()),
                ("message", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ("class_name", "method_name"),
                "unique_together": {("class_name", "method_name", "content_type", "object_id", "validated_attribute")},
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
    ]
