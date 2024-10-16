# Generated by Django 3.2.20 on 2023-08-23 19:02

import nautobot.core.models.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0098_rename_data_jobresult_result"),
        ("nautobot_data_validation_engine", "0004_created_datetime"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="minmaxvalidationrule",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="regularexpressionvalidationrule",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="requiredvalidationrule",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="uniquevalidationrule",
            name="slug",
        ),
        migrations.AlterField(
            model_name="datacompliance",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AlterField(
            model_name="minmaxvalidationrule",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AlterField(
            model_name="regularexpressionvalidationrule",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AlterField(
            model_name="requiredvalidationrule",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AlterField(
            model_name="uniquevalidationrule",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
    ]
