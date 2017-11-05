from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import ListView

from .models import Student


def students(request):
    students = Student.objects.all()
    paginator = Paginator(students, 100, orphans=5)  # Show 100 students per page

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

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
    orphans = 5

    def get_context_data(self):
        ctx = super().get_context_data()
        current_page = ctx.pop('page_obj', None)
        ctx['current_page'] = current_page
        return ctx
