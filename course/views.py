from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Course, CourseBook
from django.core.paginator import Paginator, PageNotAnInteger,  EmptyPage
from django.contrib import messages
from fmb.settings import API_KEY
import requests


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
    
    return render(request=request, template_name='home.html', context={'courses': object_courses, 'paginator': paginator})


def detail(request, id):
    course = get_object_or_404(Course, id=id)
    course_book = CourseBook.objects.filter(courseid=id)

    if course_book.exists():
        url = "https://dapi.kakao.com/v3/search/book"
        rest_api_key = API_KEY['kakao_rest_key']
        header = {'Authorization': 'KakaoAK ' + rest_api_key}

        books = []
        for i in course_book.values():
            book = Book.objects.get(bookid=i['bookid_id'])
            params = {'query': book.bookname, 'sort': 'accuracy', 'target': 'title'}
            result = requests.get(url, headers=header, params=params).json()
            books.append(result)

        context = {'course': course, 'course_book': course_book, 'book': books}
    else:
        messages.error(request, '해당 강좌는 등록된 서적이 없습니다.')
        context = {'course': course}
    return render(request=request, template_name='detail.html', context=context)
