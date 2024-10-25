# Generated by Django 5.1.2 on 2024-10-24 19:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('idayear', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'tblacademicyear',
            },
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('idemotion', models.AutoField(primary_key=True, serialize=False)),
                ('emotionname', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tblemotion',
            },
        ),
        migrations.CreateModel(
            name='ErrorLevel',
            fields=[
                ('iderrorlevel', models.AutoField(primary_key=True, serialize=False)),
                ('errorlevelname', models.CharField(max_length=255)),
                ('errorlevelabbrev', models.CharField(blank=True, max_length=30, null=True)),
                ('errorlevelvalue', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'tblerrorlevel',
            },
        ),
        migrations.CreateModel(
            name='PosTag',
            fields=[
                ('idpostag', models.AutoField(primary_key=True, serialize=False)),
                ('tagtext', models.TextField()),
                ('tagtextrussian', models.TextField()),
                ('tagtextabbrev', models.TextField()),
                ('tagcolor', models.CharField(max_length=7)),
            ],
            options={
                'db_table': 'tblpostag',
            },
        ),
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('idreason', models.AutoField(primary_key=True, serialize=False)),
                ('reasonname', models.CharField(max_length=255)),
                ('reasonabbrev', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'tblreason',
            },
        ),
        migrations.CreateModel(
            name='Rights',
            fields=[
                ('idrights', models.AutoField(primary_key=True, serialize=False)),
                ('rightsname', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tblrights',
            },
        ),
        migrations.CreateModel(
            name='TextType',
            fields=[
                ('idtexttype', models.AutoField(primary_key=True, serialize=False)),
                ('texttypename', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tbltexttype',
            },
        ),
        migrations.CreateModel(
            name='WritePlace',
            fields=[
                ('idwriteplace', models.AutoField(primary_key=True, serialize=False)),
                ('writeplacename', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tblwriteplace',
            },
        ),
        migrations.CreateModel(
            name='WriteTool',
            fields=[
                ('idwritetool', models.AutoField(primary_key=True, serialize=False)),
                ('writetoolname', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'tblwritetool',
            },
        ),
        migrations.CreateModel(
            name='ErrorTag',
            fields=[
                ('iderrortag', models.AutoField(primary_key=True, serialize=False)),
                ('tagtext', models.TextField()),
                ('tagtextrussian', models.TextField()),
                ('tagtextabbrev', models.TextField()),
                ('tagcolor', models.CharField(max_length=7)),
                ('idtagparent', models.ForeignKey(blank=True, db_column='idtagparent', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.errortag')),
            ],
            options={
                'db_table': 'tblerrortag',
            },
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('iderror', models.AutoField(primary_key=True, serialize=False)),
                ('correct', models.TextField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('changedate', models.DateField(blank=True, null=True)),
                ('iderrorlevel', models.ForeignKey(blank=True, db_column='iderrorlevel', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.errorlevel')),
                ('iderrortag', models.ForeignKey(db_column='iderrortag', on_delete=django.db.models.deletion.CASCADE, to='db_editor.errortag')),
                ('idreason', models.ForeignKey(blank=True, db_column='idreason', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.reason')),
            ],
            options={
                'db_table': 'tblerror',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('idgroup', models.AutoField(primary_key=True, serialize=False)),
                ('groupname', models.CharField(max_length=10)),
                ('studycourse', models.SmallIntegerField()),
                ('idayear', models.ForeignKey(db_column='idayear', on_delete=django.db.models.deletion.CASCADE, to='db_editor.academicyear')),
            ],
            options={
                'db_table': 'tblgroup',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('iduser', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('lastname', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('middlename', models.CharField(blank=True, max_length=100, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('gender', models.BooleanField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('idrights', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db_editor.rights')),
            ],
            options={
                'db_table': 'tbluser',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('idstudent', models.AutoField(primary_key=True, serialize=False)),
                ('idgroup', models.ForeignKey(db_column='idgroup', on_delete=django.db.models.deletion.CASCADE, to='db_editor.group')),
                ('iduser', models.ForeignKey(db_column='iduser', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tblstudent',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('idtext', models.AutoField(primary_key=True, serialize=False)),
                ('header', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('createdate', models.DateField(blank=True, null=True)),
                ('modifieddate', models.DateField(blank=True, null=True)),
                ('educationlevel', models.IntegerField(blank=True, null=True)),
                ('textgrade', models.IntegerField(blank=True, null=True)),
                ('completeness', models.IntegerField(blank=True, null=True)),
                ('structure', models.IntegerField(blank=True, null=True)),
                ('coherence', models.IntegerField(blank=True, null=True)),
                ('selfrating', models.IntegerField(blank=True, null=True)),
                ('selfassesment', models.IntegerField(blank=True, null=True)),
                ('poscheckflag', models.BooleanField(blank=True, null=True)),
                ('errorcheckflag', models.BooleanField(blank=True, null=True)),
                ('poscheckdate', models.DateField(blank=True, null=True)),
                ('errorcheckdate', models.DateField(blank=True, null=True)),
                ('idemotion', models.ForeignKey(blank=True, db_column='idemotion', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.emotion')),
                ('idstudent', models.ForeignKey(db_column='idstudent', on_delete=django.db.models.deletion.CASCADE, to='db_editor.student')),
                ('idusererrorcheck', models.ForeignKey(blank=True, db_column='idusererrorcheck', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='errorcheck_texts', to=settings.AUTH_USER_MODEL)),
                ('iduserposcheck', models.ForeignKey(blank=True, db_column='iduserposcheck', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poscheck_texts', to=settings.AUTH_USER_MODEL)),
                ('iduserteacher', models.ForeignKey(blank=True, db_column='iduserteacher', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_texts', to=settings.AUTH_USER_MODEL)),
                ('idtexttype', models.ForeignKey(blank=True, db_column='idtexttype', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.texttype')),
                ('idwriteplace', models.ForeignKey(blank=True, db_column='idwriteplace', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.writeplace')),
                ('idwritetool', models.ForeignKey(blank=True, db_column='idwritetool', null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.writetool')),
            ],
            options={
                'db_table': 'tbltext',
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('idsentence', models.AutoField(primary_key=True, serialize=False)),
                ('sentensetext', models.TextField()),
                ('ordernumber', models.IntegerField()),
                ('idtext', models.ForeignKey(db_column='idtext', on_delete=django.db.models.deletion.CASCADE, to='db_editor.text')),
            ],
            options={
                'db_table': 'tblsentence',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('idtoken', models.AutoField(primary_key=True, serialize=False)),
                ('tokentext', models.TextField()),
                ('tokenordernumber', models.IntegerField()),
                ('idpostag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_editor.postag')),
                ('idsentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='db_editor.sentence')),
            ],
            options={
                'db_table': 'tbltoken',
            },
        ),
        migrations.CreateModel(
            name='ErrorToken',
            fields=[
                ('iderrortoken', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('iderror', models.ForeignKey(db_column='iderror', on_delete=django.db.models.deletion.CASCADE, to='db_editor.error')),
                ('idtoken', models.ForeignKey(db_column='idtoken', on_delete=django.db.models.deletion.CASCADE, to='db_editor.token')),
            ],
            options={
                'db_table': 'tblerrortoken',
            },
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['idsentence'], name='tbltoken_idsente_a57a42_idx'),
        ),
        migrations.AddIndex(
            model_name='token',
            index=models.Index(fields=['idpostag'], name='tbltoken_idposta_ba260e_idx'),
        ),
    ]
