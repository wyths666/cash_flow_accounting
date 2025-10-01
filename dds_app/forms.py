from django import forms
from .models import DDSRecord, Category, Subcategory, Status, Type

class DDSRecordForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,  # Необязательное поле
        label="Дата создания записи"
    )

    class Meta:
        model = DDSRecord
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        labels = {
            'status': 'Статус',
            'type': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма',
            'comment': 'Комментарий',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.type.category_set.all()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.date:  # Если дата не указана — ставим текущую
            from datetime import date
            instance.date = date.today()
        if commit:
            instance.save()
        return instance

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Название',
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        labels = {
            'name': 'Название',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        labels = {
            'name': 'Название',
            'type': 'Тип',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сделаем поле "type" обязательным
        self.fields['type'].required = True


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        labels = {
            'name': 'Название',
            'category': 'Категория',
        }