
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel('HardwareUnit', 'Equipment')
    ]
