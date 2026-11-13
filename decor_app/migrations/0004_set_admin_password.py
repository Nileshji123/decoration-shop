from django.db import migrations

def update_admin_password(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    try:
        user = User.objects.get(username='piyush')
        user.set_password('Piyush@98765')
        user.is_superuser = True
        user.is_staff = True
        user.save()
    except User.DoesNotExist:
        User.objects.create_superuser('piyush', 'admin@example.com', 'Piyush@98765')

class Migration(migrations.Migration):

    dependencies = [
        ('decor_app', '0003_decoration_item_etc'),  # Yahan apni sabse last wali migration file ka exact naam daal dena jo screen par dikh rahi hai
    ]

    operations = [
        migrations.RunPython(update_admin_password),
    ]