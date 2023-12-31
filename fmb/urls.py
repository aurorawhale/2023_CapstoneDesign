"""fmb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import course.views as course

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', course.main, name='main'),
    path('course', course.main, name='main'),
    path('detail/<int:id>/', course.detail, name='detail'),
    path('search/<int:bookid>/', course.search, name='search'),
    path('recommend/<int:course_id>/<int:book_id>/', course.recommend, name='recommend'),
]
