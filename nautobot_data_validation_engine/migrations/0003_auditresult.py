# Generated by Django 3.2.18 on 2023-04-18 16:24

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import nautobot.extras.models.mixins
import taggit.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('extras', '0053_relationship_required_on'),
        ('nautobot_data_validation_engine', '0002_required_unique_types_regex_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('_custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('audit_class_name', models.CharField(max_length=100)),
                ('last_validation_date', models.DateTimeField(auto_now=True)),
                ('object_id', models.CharField(max_length=200)),
                ('validated_attribute', models.CharField(blank=True, max_length=100, null=True)),
                ('validated_attribute_value', models.CharField(blank=True, max_length=200, null=True)),
                ('expected_attribute_value', models.CharField(blank=True, max_length=200, null=True)),
                ('valid', models.BooleanField()),
                ('message', models.TextField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'unique_together': {('audit_class_name', 'content_type', 'object_id', 'validated_attribute')},
            },
            bases=(models.Model, nautobot.extras.models.mixins.DynamicGroupMixin, nautobot.extras.models.mixins.NotesMixin),
        ),
    ]
