from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_gallery'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ] 