from django.core.paginator import InvalidPage, Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic import ListView, View

from .models import Student


def students(request):
    students = Student.objects.all()
    paginator = Paginator(students, 100, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator
    }

    return render(request, 'main/students.html', context)


class StudentListView(ListView):
    model = Student
    template_name = 'main/students.html'
    paginate_by = 100
    paginate_orphans = 5

    def get_context_data(self):
        ctx = super().get_context_data()
        current_page = ctx.pop('page_obj', None)
        ctx['current_page'] = current_page
        return ctx


def studentsjson(request):
    students = Student.objects.values('id', 'first_name', 'last_name', 'gender', 'dob')
    paginator = Paginator(students, 100, orphans=5)

    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        page = int(page) if page.isdigit() else page
        context = {
           'page_number': page,
           'message': str(e)
        }
        return JsonResponse(context, status=404)
    context = {
        'students': list(current_page)
    }
    return JsonResponse(context)


class StudentJsonView(View):

    def get(self, *args, **kwargs):
        students = Student.objects.values('id', 'first_name', 'last_name', 'gender', 'dob')
        paginator = Paginator(students, 100, orphans=5)

        page = self.request.GET.get('page') or 1
        try:
            current_page = paginator.page(page)
        except InvalidPage as e:
            page = int(page) if page.isdigit() else page
            context = {
                'page_number': page,
                'message': str(e)
            }
            return JsonResponse(context, status=404)

        context = {
            'students': list(current_page)
        }
        return JsonResponse(context)
