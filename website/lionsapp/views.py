from django.shortcuts import render
from .search import *
from django.views.generic import CreateView, UpdateView
from .models import Habbit, HabbitCheckIn
from .forms import HabbitForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse
from datetime import datetime
from django.forms import Textarea

@login_required
def index(request):

    good_habbits = Habbit.objects.filter(user_id= request.user.id, is_good=True)
    bad_habbits = Habbit.objects.filter(user_id= request.user.id, is_good=False)

    for h in good_habbits:
        checkins = HabbitCheckIn.objects.filter( habbit_id= h.id).order_by('-check_in_date')[:1]
        if len(checkins) > 0:
            print('found check in')
            h.is_done = True
            a = checkins[0].check_in_date.date()
            b = datetime.today().date()
            delta = (b - a).days
            h.good_days = abs( delta )
        else:
            h.is_done = False
            h.good_days = 0

    context = {
        'good_habbits': good_habbits
    }
    return render(request, 'index.html', context)

def checkin(request, id):
    checkin = HabbitCheckIn(habbit_id = id)
    try:
        checkin.save()
    except Exception as e:
         print(str(e))

    return HttpResponse(checkin.check_in_date)

def undo_checkin(request, id):
    print(datetime.today())
    print("id" + str(id))
    print(datetime.today().date())
    HabbitCheckIn.objects.filter(check_in_date__gte=datetime.today().date(), habbit_id = id).delete()

    return HttpResponse()

class HabbitCreate(CreateView):
    model = Habbit
    template_name  ="new_habbit_form.html"
    # fields = ['name', 'image', 'description']
    form_class = HabbitForm
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.is_good = True
        object.save()
        return super(HabbitCreate, self).form_valid(form)
    def get_success_url(self):
        return "/"

def delete_habbit(request, id):
    print("id" + str(id))
    Habbit.objects.filter(id = id).delete()
    return HttpResponse("Ok")
