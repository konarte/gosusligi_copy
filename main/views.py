from django.http import HttpResponse
from django.shortcuts import render

from main.models import PageInfo


def index(request, uuid):
    # really hope this works
    page_object = PageInfo.objects.get(uuid=uuid)
    name = page_object.name.split()
    # TODO: если не отчества то баг, пофиксить

    context = {"sensetive": {"name1": name[0][0] + '*' * (len(name[0]) - 1),
                             "name2": name[1][0] + '*' * (len(name[1]) - 1),
                             "name3": name[2][0] + '*' * (len(name[2]) - 1),
                             "date_of_birth": page_object.date_of_birth,
                             "first_two_passport_numbers": page_object.first_two_passport_numbers,
                             "last_three_passport_numbers": page_object.last_three_passport_numbers}}
    return render(request, 'index.html', context=context)


