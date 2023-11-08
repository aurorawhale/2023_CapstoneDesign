from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Course, CourseBook
from django.core.paginator import Paginator, PageNotAnInteger,  EmptyPage
from django.contrib import messages
from fmb.settings import API_KEY
import requests
from . import get_store_info
from . import naver_api


# Create your views here.
def home(request):
    courses = Course.objects.all()

    if campus := request.GET.get('campus'):
        courses = courses.filter(campus__contains=campus)

    if course_number := request.GET.get('course_number'):
        courses = courses.filter(courseid__contains=course_number)

    if section := request.GET.get('section'):
        courses = courses.filter(subid__contains=section)

    if classification := request.GET.get('classification'):
        courses = courses.filter(division__contains=classification)

    if department := request.GET.get('department'):
        courses = courses.filter(department__contains=department)

    if course_name := request.GET.get('course_name'):
        courses = courses.filter(coursename__contains=course_name)

    if professor := request.GET.get('professor'):
        courses = courses.filter(professor__contains=professor)

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
    page = request.GET.get('page', '1')
    course = get_object_or_404(Course, id=id)
    course_book = CourseBook.objects.filter(courseid=id)

    if course_book.exists():
        count = course_book.count
        paginator = Paginator(course_book, 5)
        course_book = paginator.get_page(page)

        url = "https://dapi.kakao.com/v3/search/book"
        rest_api_key = API_KEY['kakao_rest_key']
        header = {'Authorization': 'KakaoAK ' + rest_api_key}

        books = []
        for i in course_book:
            book = Book.objects.get(bookid=i.bookid_id)
            params = {'query': book.bookname, 'sort': 'accuracy'}
            result = requests.get(url, headers=header, params=params).json()
            if 'errorType' in result:
                books.append('error')
            elif result['documents']:
                if result['documents'][0]['status']:
                    store = get_store_info.get(result['documents'][0]['url'])

                else:
                    store = 'none'
                result['documents'][0]['store'] = store
                books.append(result['documents'][0])

            else:
                books.append('none')

        context = {'course': course, 'course_book': course_book, 'book': books, 'count': count}
    else:
        messages.error(request, '해당 강좌는 등록된 도서가 없습니다.')
        context = {'course': course}
    return render(request=request, template_name='course/detail.html', context=context)


def search(request, book):
    page = request.GET.get('page', '1')
    if book == ' ':
        kw = request.GET.get('kw', '')
    else:
        kw = book
    target = request.GET.get('target', '')

    book_list = []
    meta = []
    if kw:
        url = "https://dapi.kakao.com/v3/search/book"
        rest_api_key = API_KEY['kakao_rest_key']
        header = {'Authorization': 'KakaoAK ' + rest_api_key}
        params = {'query': kw, 'sort': 'accuracy', 'size': 5, 'page': page, 'target': target}
        result = requests.get(url, headers=header, params=params).json()
        if not 'errorType' in result:
            meta = result['meta']
            meta['total_page'] = meta['total_count'] // 5 if meta['total_count'] % 5 == 0 else meta['total_count'] // 5 + 1
            meta['current_page'] = int(page)

            book_list = result['documents']
            for book in book_list:
                if book['status']:
                    store = get_store_info.get(book['url'])
                else:
                    store = 'none'
                book['store'] = store
        else:
            book_list = {}
            meta = {'error': 1}

    context = {'book_list': book_list, 'page': page, 'meta': meta, 'kw': kw}
    return render(request=request, template_name='course/search.html', context=context)


def recommend(request, course_id, book_id):
    course = get_object_or_404(Course, id=course_id)
    course_book = get_object_or_404(Book, bookid=book_id)

    # naver api tools
    client_id = API_KEY['naver_id']
    client_secret = API_KEY['naver_secret']
    header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret,
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    # check bookname language
    bookname = course_book.bookname
    langcode = naver_api.is_korean(bookname)

    if langcode == -1:
        messages.error(request, '추천 도서를 찾는 과정에서 오류가 발생하였습니다')
        context = {'course': course, 'course_book': course_book}
        return render(request,template_name='course/recommend.html', context=context)
    elif langcode != 'ko':
        # translate bookname to korean
        result = naver_api.papago_trans(langcode, bookname)
        if result == -1:
            messages.error(request, '추천 도서를 찾는 과정에서 오류가 발생하였습니다')
            context = {'course': course, 'course_book': course_book}
            return render(request, template_name='course/recommend.html', context=context)
        else:
            bookname = result

    # 유사성 체크
    keyword = ''

    # recommend book
    recommend_book = {}

    # recommend course
    recommend_course = Course.objects.filter(coursename__contains=course.coursename[:3])

    context = {'course': course, 'course_book': course_book,
               'recommend_book': recommend_book, 'recommend_course': recommend_course}
    return render(request=request, template_name='course/recommend.html', context=context)
