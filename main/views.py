from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from .forms import *
from .models import *
from django.contrib import messages
from .modules.hashutils import *
import datetime

from django.http import HttpResponseRedirect

from .modules.utils import *

ALL_MODELS = {
    "students": Student,
    "workers": Worker,
    "books": Book,
    "groups": Group,
    "roles": Role,
    "logs": Log
}


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if(get_current_user(request)):
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {

        })
    
    def post(self, request):
        login = request.POST["login"]
        password = request.POST["password"]
        login_form = LoginForm({
            "login": login,
            "password": password
        })

        if(login_form.is_valid()):
            try:                
                user = User.objects.get(login=login, password=make_pw_hash(password))
                request.session["current_user"] = user.id
                return redirect(reverse("main:index"))
            except:
                messages.error(message="Неверный логин или папроль!", request=request)
                return redirect(reverse("main:login"))
        else:
            errors = login_form.errors.as_data()            
            key = next(iter(errors))
            error_message = errors[key][0].messages[0].replace("this value", key).replace("This", key)
            
            messages.error(message=error_message, request=request)
            return redirect(reverse("main:login"))


class LogoutView(View):
    def get(self, request):
        pass
    
    def post(self, request):
        del request.session["current_user"]
        return redirect(reverse("main:login"))


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        if(get_current_user(request)):
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {
            "roles": Role.objects.all()
        })
    
    def post(self, request):
        login = request.POST["login"]
        password = request.POST["password"]
        age = request.POST["age"]
        fullname = request.POST["fullname"]
        role = request.POST["role"]

        register_form = RegisterForm({
            "login": login,
            "password": password,
            "age": age,
            "fullname": fullname,
            "role": role
        })

        if(register_form.is_valid()):
            try:
                user = User.objects.get(login=login, password=password)
                if user:
                    messages.error(message="Такой пользовватель уже существует!", request=request)
                    return redirect(reverse("main:register"))                
            except:
                role_obj = Role.objects.get(name=role)
                user = User.objects.create(login=login, password=make_pw_hash(password), role=role_obj, fullname=fullname)
                if role == "student":                    
                    Student.objects.create(user=user)
                elif role == "worker":                    
                    Worker.objects.create(user=user)
                
                return redirect(reverse("main:login"))
        else:
            errors = register_form.errors.as_data()            
            key = next(iter(errors))
            error_message = errors[key][0].messages[0].replace("this value", key).replace("This", key)

            messages.error(message=error_message, request=request)
            return redirect(reverse("main:register"))


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):
            
            q = get_or_none(request, "qs", "")            
            menu_item = "students"
            
            filtered = Student.objects.all()
            if q:
                filtered = filter_model(Student, q)

            data = []
            fields = ["id", "age", "group", "user_fullname",  "user_login", "user_password", "user_role"]                        
            fields_for_create = ["age", "fullname", "login", "password"]
            

            for item in filtered:
                group_name = None if not item.group else item.group.name
                data.append([item.id, item.age, group_name, item.user.fullname, item.user.login, item.user.password, item.user.role.ru_name])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "groups": Group.objects.all(),
                "roles": Role.objects.all(),
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        age = post_or_none(request, "age")
        fullname = post_or_none(request, "fullname")
        login = post_or_none(request, "login")
        password = post_or_none(request, "password")

        group_id = post_or_none(request, "group")
        group = Group.objects.get(id=group_id)
        role_id = post_or_none(request, "role")
        role = Role.objects.get(id=role_id)

        user = User.objects.create(fullname=fullname, login=login, password=make_pw_hash(password), role=role)
        user.save()
        student = Student.objects.create(age=age, user=user, group=group)
        student.save()

        messages.success(message="Студент успешно создан!", request=request)
        return redirect(reverse("main:index"))



class WorkersView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):            
            q = get_or_none(request, "qs", "")            
            menu_item = "workers"
            
            filtered = Worker.objects.all()
            if q:
                filtered = filter_model(Worker, q)

            data = []
            fields = ["id", "work_period", "user_fullname",  "user_login", "user_password", "user_role"]                        
            fields_for_create = ["work_period", "fullname", "login", "password"]

            for item in filtered:
                data.append([item.id, item.work_period, item.user.fullname, item.user.login, item.user.password, item.user.role.name])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "roles": Role.objects.all(),
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        work_period = post_or_none(request, "work_period")
        fullname = post_or_none(request, "fullname")
        login = post_or_none(request, "login")
        password = post_or_none(request, "password")
        
        role_id = post_or_none(request, "role")
        role = Role.objects.get(id=role_id)

        user = User.objects.create(fullname=fullname, login=login, password=make_pw_hash(password), role=role)
        user.save()
        student = Worker.objects.create(work_period=work_period, user=user, )
        student.save()

        messages.success(message="Работник успешно создан!", request=request)
        return redirect(reverse("main:workers"))


class BooksView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):            
            q = get_or_none(request, "qs", "")            
            menu_item = "books"
            
            filtered = Book.objects.all()
            if q:
                filtered = filter_model(Book, q)

            data = []
            fields = ["id", "name", "author",  "year"]                        
            fields_for_create = ["name", "author", "year"]

            for item in filtered:
                data.append([item.id, item.name, item.author, item.year])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        name = post_or_none(request, "name")
        author = post_or_none(request, "author")
        year = post_or_none(request, "year")        
        
        book = Book.objects.create(name=name, author=author, year=year)
        book.save()

        messages.success(message="Книга успешно создана!", request=request)
        return redirect(reverse("main:books"))


class LogsView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):            
            q = get_or_none(request, "qs", "")            
            menu_item = "logs"
            
            filtered = Log.objects.all()
            if q:
                filtered = filter_model(Log, q)

            data = []
            fields = ["id", "student", "book",  "worker", "when", "log_type"]     
            fields_for_create = ["when", "log_type"]               

            for item in filtered:                
                data.append([item.id, item.student.user.fullname, item.book.name, item.worker.user.fullname,  item.when, item.log_type])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "students": Student.objects.all(),
                "books": Book.objects.all(),
                "workers": Worker.objects.all(),
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        when = post_or_none(request, "when")
        when = datetime.datetime.strptime(when)
        log_type = post_or_none(request, "log_type")
        
        student_id = post_or_none(request, "student")
        student = Student.objects.get(id=student_id)

        book_id = post_or_none(request, "book")
        book = Book.objects.get(id=book_id)

        worker_id = post_or_none(request, "worker")
        worker = Worker.objects.get(id=worker_id)
                
        log = Log.objects.create(student=student, book=book, worker=worker, when=when, log_type=log_type)
        log.save()

        messages.success(message="Оперция успешно создана!", request=request)
        return redirect(reverse("main:logs"))


class GroupsView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):            
            q = get_or_none(request, "qs", "")            
            menu_item = "groups"
            
            filtered = Group.objects.all()
            if q:
                filtered = filter_model(Group, q)

            data = []
            fields = ["id", "name"]    
            fields_for_create = ["name"]                    

            for item in filtered:
                data.append([item.id, item.name])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        name = post_or_none(request, "name")                
        
        group = Group.objects.create(name=name)
        group.save()

        messages.success(message="Группа успешно создана!", request=request)
        return redirect(reverse("main:groups"))


class RolesView(View):
    template_name = "index.html"

    def get(self, request):
        user = get_current_user(request)
        if(user):            
            q = get_or_none(request, "qs", "")            
            menu_item = "roles"
            
            filtered = Role.objects.all()
            if q:
                filtered = filter_model(Role, q)

            data = []
            fields = ["id", "name", "ru_name"]  
            fields_for_create = ["name", "ru_name"]                      

            for item in filtered:
                data.append([item.id, item.name, item.ru_name])
            
            return render(request, self.template_name, {
                "data": data,
                "fields": fields,
                "fields_for_create": fields_for_create,
                "current_user": user,
                "menu_item": menu_item,
                "qs": q,
            })
        else:
            return redirect(reverse("main:login"))
    
    def post(self, request):
        name = post_or_none(request, "name")   
        ru_name = post_or_none(request, "ru_name")                
        
        role = Role.objects.create(name=name, ru_name=ru_name)
        role.save()

        messages.success(message="Роль успешно создана!", request=request)
        return redirect(reverse("main:roles"))


class DeleteView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        menu_item = post_or_none(request, "menu_item")   
        _id = post_or_none(request, "id")   
        model, _ = get_model_by_name(menu_item)
        model.objects.get(id=_id).delete()

        messages.success(message="Объект успешно удален!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class StudentEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        student_id = post_or_none(request, "id")
        
        age = post_or_none(request, "age")
        fullname = post_or_none(request, "fullname")
        login = post_or_none(request, "login")
        password = post_or_none(request, "password")

        group_id = post_or_none(request, "group")
        group = Group.objects.get(id=group_id)
        role_id = post_or_none(request, "role")
        role = Role.objects.get(id=role_id)

        student = Student.objects.get(id=student_id)
        student.age = age
        student.user.fullname = fullname
        student.user.login = login
        student.user.password = password
        student.group = group
        student.user.role = role
        student.user.save()
        student.save()

        messages.success(message="Студент успешно обновлен!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WorkerEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        _id = post_or_none(request, "id")
        
        work_period = post_or_none(request, "work_period")
        fullname = post_or_none(request, "fullname")
        login = post_or_none(request, "login")
        password = post_or_none(request, "password")
        
        role_id = post_or_none(request, "role")
        role = Role.objects.get(id=role_id)

        
        worker = Worker.objects.create(id=_id)
        worker.work_period = work_period
        worker.user.fullname = fullname
        worker.user.login = login
        worker.user.password = password
        worker.user.role = role
        worker.save()

        messages.success(message="Работник успешно обновлен!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BookEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        book_id = post_or_none(request, "id")
        
        name = post_or_none(request, "name")
        author = post_or_none(request, "author")
        year = post_or_none(request, "year")        
        
        book = Book.objects.get(id=book_id)
        book.name = name
        book.author = author
        book.year = year
        book.save()

        messages.success(message="Книга успешно обновлена!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        _id = post_or_none(request, "id")
        
        when = post_or_none(request, "when")
        when = datetime.datetime.strptime(when)
        log_type = post_or_none(request, "log_type")
        
        student_id = post_or_none(request, "student")
        student = Student.objects.get(id=student_id)

        book_id = post_or_none(request, "book")
        book = Book.objects.get(id=book_id)

        worker_id = post_or_none(request, "worker")
        worker = Worker.objects.get(id=worker_id)
                
        log = Log.objects.get(id=_id)
        log.when = when
        log.log_type = log_type
        log.student = student
        log.book = book
        log.worker = worker
        log.save()

        messages.success(message="Оперция успешно обновлена!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GroupEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        _id = post_or_none(request, "id")
                
        name = post_or_none(request, "name")
       
        group = Group.objects.get(id=_id)
        group.name = name
        group.save()

        messages.success(message="Группа успешно обновлена!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RoleEditView(View):    
    def get(self, request):        
        return redirect(reverse("main:index"))
    
    def post(self, request):
        _id = post_or_none(request, "id")
                
        name = post_or_none(request, "name")
        ru_name = post_or_none(request, "ru_name")
       
        role = Role.objects.get(id=_id)
        role.name = name
        role.ru_name = ru_name
        role.save()

        messages.success(message="Роль успешно обновлена!", request=request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))