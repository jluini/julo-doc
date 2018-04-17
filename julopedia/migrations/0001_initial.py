# Generated by Django 2.0.4 on 2018-04-17 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_key', models.CharField(max_length=200)),
                ('article_title', models.CharField(max_length=200)),
                ('article_type', models.IntegerField(default=0)),
                ('article_body', models.CharField(blank=True, default='', max_length=15000)),
                ('article_modification_date', models.DateTimeField(verbose_name='date modified')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide_key', models.CharField(default='guide1', max_length=200)),
                ('guide_title', models.CharField(default='', max_length=200)),
                ('guide_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='julopedia.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='julopedia.Article')),
                ('node_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='julopedia.Node')),
            ],
        ),
        migrations.AddField(
            model_name='guide',
            name='guide_root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='julopedia.Node'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='julopedia.Author'),
        ),
    ]
