from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Course, CourseBook
from django.core.paginator import Paginator, PageNotAnInteger,  EmptyPage
from django.contrib import messages
from fmb.settings import API_KEY
import requests


# Create your views here.
def home(request):
    courses = Course.objects.all()

    if campus := request.GET.get('campus'):
        courses = courses.filter(campus=campus)

    if course_number := request.GET.get('course_number'):
        courses = courses.filter(courseid=course_number)

    if section := request.GET.get('section'):
        courses = courses.filter(subid=section)

    if classification := request.GET.get('classification'):
        courses = courses.filter(division=classification)

    if department := request.GET.get('department'):
        courses = courses.filter(department=department)

    if course_name := request.GET.get('course_name'):
        courses = courses.filter(coursename=course_name)

    if professor := request.GET.get('professor'):
        courses = courses.filter(professor=professor)

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

    return render(request=request, template_name='course/home.html', context={'courses': object_courses, 'paginator': paginator})


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
            params = {'query': book.bookname, 'sort': 'accuracy'}
            result = requests.get(url, headers=header, params=params).json()
            if 'errorType' in result:
                books.append('error')
            elif result['documents']:
                books.append(result['documents'][0])
            else:
                books.append('none')

        context = {'course': course, 'course_book': course_book, 'book': books}
    else:
        messages.error(request, '해당 강좌는 등록된 서적이 없습니다.')
        context = {'course': course}
    return render(request=request, template_name='course/detail.html', context=context)
