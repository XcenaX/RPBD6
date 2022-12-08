from django.db import models
from main.modules.hashutils import *

class Role(models.Model):
    name = models.TextField(default="")
    ru_name  = models.TextField(default="")

    def __str__(self) -> str:
        return self.ru_name

class User(models.Model):
    login = models.TextField(default="")
    password = models.TextField(default="")
    fullname = models.TextField(default="")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.fullname


class Worker(models.Model):    
    work_period = models.IntegerField(default=0, max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.fullname


class Group(models.Model):
    name = models.TextField(default="")

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    age = models.IntegerField(default=0, max_length=2)
    group  = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        if self.user is not None:
            return self.user.fullname
        return "Student"+str(self.id)


class Book(models.Model):
    name = models.TextField(default="")
    author = models.TextField(default="")
    year = models.IntegerField(default=2000, max_length=4)

    def __str__(self) -> str:
        return self.name

class Log(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True, blank=True)
    log_type = models.TextField(default="")

    def __str__(self) -> str:
        return self.when + " | Worker: " + self.worker.user.fullname + " | Student: " + self.student.user.fullname + " | Book: " + self.book.name