from django.shortcuts import render, get_object_or_404
from .models import Book, Course, CourseBook
from django.core.paginator import Paginator, PageNotAnInteger,  EmptyPage

# Create your views here.
def home(request):
    courses = Course.objects.all()
    page = request.GET.get('page')
    
    paginator = Paginator(courses, 10)
    
    try:
        object_courses = paginator.get_page(page)
    except PageNotAnInteger:
        page = 1
        object_courses = paginator.get_page(page)
    except EmptyPage:
        page = paginator.num_pages
        object_courses = paginator.get_page(page)
        
    # index_range = int(page) // 10
    # if index_range == int(page)/10:
    #     custom_range = range(index_range*10-9, 1+index_range*10)
    # else:
    #     custom_range = range(1+index_range*10, 11+index_range*10)
    
    return render(request=request, template_name='home.html', context={'courses':object_courses, 'paginator':paginator})

def detail(request, id):
    course = get_object_or_404(Course, id=id)
    course_book = get_object_or_404(CourseBook, courseid=id)
    book = get_object_or_404(Book, bookid=course_book.bookid)
    return render(request=request, template_name='detail.html', context={'course':course, 'course_book':course_book, 'book':book})