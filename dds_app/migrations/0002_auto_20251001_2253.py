from django.db import migrations

def create_initial_data(apps, schema_editor):
    Status = apps.get_model('dds_app', 'Status')
    Type = apps.get_model('dds_app', 'Type')
    Category = apps.get_model('dds_app', 'Category')
    Subcategory = apps.get_model('dds_app', 'Subcategory')

    # Создаем типы
    type_income, _ = Type.objects.get_or_create(name="Пополнение")
    type_expense, _ = Type.objects.get_or_create(name="Списание")

    # Создаем статусы
    Status.objects.get_or_create(name="Бизнес")
    Status.objects.get_or_create(name="Личное")
    Status.objects.get_or_create(name="Налог")

    # Создаем категории "Пополнение"
    type_income = Type.objects.get(name="Пополнение")
    cat_income, _ = Category.objects.get_or_create(name="Доходы", type=type_income)

    # Подкатегории "Пополнение"
    Subcategory.objects.get_or_create(name="Зарплата", category=cat_income)
    Subcategory.objects.get_or_create(name="Дивиденды", category=cat_income)

    # Категории "Списание"
    type_expense = Type.objects.get(name="Списание")
    cat_expense, _ = Category.objects.get_or_create(name="Расходы", type=type_expense)
    cat_infra, _ = Category.objects.get_or_create(name="Инфраструктура", type=type_expense)
    cat_marketing, _ = Category.objects.get_or_create(name="Маркетинг", type=type_expense)
    cat_tax, _ = Category.objects.get_or_create(name="Налоги", type=type_expense)
    # Подкатегории "Списание"
    Subcategory.objects.get_or_create(name="VPS", category=cat_infra)
    Subcategory.objects.get_or_create(name="Proxy", category=cat_infra)
    Subcategory.objects.get_or_create(name="Farpost", category=cat_marketing)
    Subcategory.objects.get_or_create(name="Avito", category=cat_marketing)
    Subcategory.objects.get_or_create(name="НДФЛ", category=cat_tax)
    Subcategory.objects.get_or_create(name="Прочее", category=cat_expense)

def reverse_initial_data(apps, schema_editor):
    Status = apps.get_model('dds_app', 'Status')
    Type = apps.get_model('dds_app', 'Type')
    Category = apps.get_model('dds_app', 'Category')
    Subcategory = apps.get_model('dds_app', 'Subcategory')

    Subcategory.objects.all().delete()
    Category.objects.all().delete()
    Type.objects.all().delete()
    Status.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('dds_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]