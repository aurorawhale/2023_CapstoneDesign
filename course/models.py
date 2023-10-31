from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Book(models.Model):
    bookid = models.AutoField(db_column='bookID', primary_key=True)  # Field name made lowercase.
    bookname = models.CharField(db_column='bookName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(max_length=100)
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'book'

    def __str__(self):
        return self.bookname

class Course(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    campus = models.CharField(max_length=15)
    courseid = models.CharField(db_column='courseID', max_length=8)  # Field name made lowercase.
    subid = models.CharField(db_column='subID', max_length=4)  # Field name made lowercase.
    division = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    coursename = models.CharField(db_column='courseName', max_length=200)  # Field name made lowercase.
    professor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'
        
    def __str__(self):
        return self.coursename


class CourseBook(models.Model):
    relationid = models.AutoField(db_column='relationID', primary_key=True)  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookID', blank=True, null=True)  # Field name made lowercase.
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'course_book'
        
    def __str__(self):
        return str(self.bookid)