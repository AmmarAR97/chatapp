# Generated by Django 4.2.5 on 2023-09-12 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('message_content_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('docs', 'Docs'), ('video', 'Video'), ('audio', 'Audio')], default='text', max_length=10)),
                ('media_file', models.FileField(upload_to='media/messages/')),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to=settings.AUTH_USER_MODEL)),
                ('parent_message', models.ForeignKey(blank=True, limit_choices_to={'parent_message': None}, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.messagerecord')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['author'], name='chat_messag_author__b15d4b_idx'), models.Index(fields=['receiver'], name='chat_messag_receive_d56900_idx'), models.Index(fields=['created_at'], name='chat_messag_created_bf728a_idx')],
            },
        ),
    ]