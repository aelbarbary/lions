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
        h.is_done_today = False
        # h.good_days = 0
        if len(checkins) > 0:
            # print(checkins[0].check_in_date.date() )
            # print(datetime.today().date())
            if checkins[0].check_in_date.date() == datetime.today().date():
                print("equals")
                h.is_done_today = True
            # last_checkin_date = checkins[0].check_in_date.date()
            # today = datetime.today().date()
            # h.good_days = abs( (today - last_checkin_date).days )

    context = {
        'good_habbits': good_habbits
    }
    return render(request, 'index.html', context)

def checkin(request, id):

    checkin = HabbitCheckIn(habbit_id = id)
    try:
        checkin.save()
        habbit = Habbit.objects.get(pk=id)
        habbit.good_for = habbit.good_for + 1
        habbit.save()
        return HttpResponse(habbit.good_for)
    except Exception as e:
         print(str(e))

    return HttpResponse(checkin.check_in_date)

def undo_checkin(request, id):
    print(datetime.today())
    print("id" + str(id))
    print(datetime.today().date())
    HabbitCheckIn.objects.filter(check_in_date__gte=datetime.today().date(), habbit_id = id).delete()
    habbit = Habbit.objects.get(pk=id)
    habbit.good_for = habbit.good_for - 1
    habbit.save()
    return HttpResponse(habbit.good_for)

class HabbitCreate(CreateView):
    model = Habbit
    template_name  ="habbit_form.html"
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
