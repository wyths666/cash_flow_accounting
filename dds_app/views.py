from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import DDSRecord, Category, Subcategory, Status, Type
from .forms import DDSRecordForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm

class DDSListView(ListView):
    model = DDSRecord
    template_name = 'dds_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('status', 'type', 'category', 'subcategory')

        # Фильтрация
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        status = self.request.GET.get('status')
        record_type = self.request.GET.get('type')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status:
            queryset = queryset.filter(status_id=status)
        if record_type:
            queryset = queryset.filter(type_id=record_type)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)

        # Сортировка
        sort = self.request.GET.get('sort', '-date')  # по умолчанию - по дате (новые сверху)
        allowed_sorts = ['date', '-date', 'amount', '-amount', 'status__name', '-status__name', 'type__name', '-type__name', 'category', '-category', 'subcategory', '-subcategory']
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        sort = self.request.GET.get('sort', '-date')
        context['current_sort'] = sort
        context['default_sort'] = '-date'  # по умолчанию
        return context

class DDSRecordCreateView(CreateView):
    model = DDSRecord
    form_class = DDSRecordForm
    template_name = 'dds_form.html'
    success_url = reverse_lazy('dds_list')

class DDSRecordUpdateView(UpdateView):
    model = DDSRecord
    form_class = DDSRecordForm
    template_name = 'dds_form.html'
    success_url = reverse_lazy('dds_list')

class DDSRecordDeleteView(DeleteView):
    model = DDSRecord
    template_name = 'dds_delete.html'
    success_url = reverse_lazy('dds_list')

def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def manage_refs(request):
    entities = {
        'status': {'model': Status, 'form': StatusForm},
        'type': {'model': Type, 'form': TypeForm},
        'category': {'model': Category, 'form': CategoryForm},
        'subcategory': {'model': Subcategory, 'form': SubcategoryForm},
    }

    forms = {key: entity['form']() for key, entity in entities.items()}

    if request.method == 'POST':
        action = request.POST.get('action')
        entity_type = request.POST.get('entity_type')

        if action and entity_type in entities:
            entity = entities[entity_type]
            Model = entity['model']
            Form = entity['form']

            if action == 'add':
                form = Form(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'{Model._meta.verbose_name} добавлен(а)')
                    return redirect('manage_refs')

            elif action == 'edit':
                obj = get_object_or_404(Model, id=request.POST.get('obj_id'))
                obj.name = request.POST.get('obj_name')
                obj.save()
                messages.success(request, f'{Model._meta.verbose_name} обновлен(а)')
                return redirect('manage_refs')

            elif action == 'delete':
                obj = get_object_or_404(Model, id=request.POST.get('obj_id'))
                obj.delete()
                messages.success(request, f'{Model._meta.verbose_name} удален(а)')
                return redirect('manage_refs')

    context = {
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'status_form': StatusForm(),
        'type_form': TypeForm(),
        'category_form': CategoryForm(),
        'subcategory_form': SubcategoryForm(),
    }

    return render(request, 'dds_manage.html', context)