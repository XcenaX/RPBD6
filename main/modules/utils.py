from ..models import *

from django.db.models import TextField, Q

def get_current_user(request):
    try:
        return User.objects.get(id=request.session["current_user"])
    except:
        return None

def get_model_fields(model):
    fields = list(model._meta.fields)
    for i in range(len(fields)):
        fields[i] = str(fields[i]).split(".")[2]
    return fields

def filter_model(model, query):
    fields = [f for f in model._meta.fields if isinstance(f, TextField)]
    queries = [Q(**{f.name+"__icontains":query}) for f in fields]

    qs = Q()
    for query in queries:
        qs = qs | query
    
    return model.objects.filter(qs)


def get_or_none(request, parameter, value_if_none=None):
    try:
        return request.GET[parameter]
    except:
        return value_if_none

def post_or_none(request, parameter, value_if_none=None):
    try:
        return request.POST[parameter]
    except:
        return value_if_none

def parameter_or_none(parameter):
    try:
        return parameter
    except:
        ""


def get_model_by_name(name):
    name = str(name)
    if name.lower().__contains__("user"):
        return User, "user"
    elif name.lower().__contains__("group"):
        return Group, "group"
    elif name.lower().__contains__("role"):
        return Role, "role"
    elif name.lower().__contains__("book"):
        return Book, "book"
    elif name.lower().__contains__("log"):
        return Log, "log"
    elif name.lower().__contains__("student"):
        return Student, "student"
    elif name.lower().__contains__("worker"):
        return Worker, "worker"
    return None, ""

def get_field(instance, field):
    field_path = field.split('.')
    attr = instance
    for elem in field_path:
        try:
            attr = getattr(attr, elem)
        except AttributeError:
            return None
    return attr
