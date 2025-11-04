from django.db import migrations, models
from django.conf import settings


def create_default_room(apps, schema_editor):
    ChatRoom = apps.get_model('api', 'ChatRoom')
    ChatRoom.objects.get_or_create(name='Общий')


def remove_default_room(apps, schema_editor):
    ChatRoom = apps.get_model('api', 'ChatRoom')
    ChatRoom.objects.filter(name='Общий').delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Chat Room',
                'verbose_name_plural': 'Chat Rooms',
            },
        ),
        migrations.CreateModel(
            name='ChatMembership',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('MODERATOR', 'Moderator'), ('MEMBER', 'Member')], default='MEMBER', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='memberships', to='api.chatroom')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='chat_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Chat Membership',
                'verbose_name_plural': 'Chat Memberships',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='messages', to='api.chatroom')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='chatmembership',
            constraint=models.UniqueConstraint(fields=('user', 'room'), name='unique_user_room_membership'),
        ),
        migrations.RunPython(create_default_room, remove_default_room),
    ]
