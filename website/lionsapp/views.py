from django.shortcuts import render
from .search import *
from django.views.generic import CreateView, UpdateView
from .models import *
from .forms import *
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
from datetime import datetime, timedelta
from django.forms import Textarea

@login_required
def index(request):

    good_traits = GoodTrait.objects.filter(user_id= request.user.id).order_by('name')
    bad_traits = BadTrait.objects.filter(user_id= request.user.id).order_by('name')

    for t in good_traits:
        checkins = GoodTraitCheckIn.objects.filter( good_trait_id= t.id).order_by('-date')[:1]
        t.is_done_today = False
        t.good_for = t.calc_good_for()
        if len(checkins) > 0:
            if checkins[0].date.date() == datetime.today().date():
                print("equals")
                t.is_done_today = True
    for t in bad_traits:
         act_out_list = BadTraitActOut.objects.filter( bad_trait_id= t.id).order_by('-date')[:1]
         t.is_done_today = False
         if len(act_out_list) > 0:
             last_act_out = act_out_list[0].date.date()
             today = datetime.today().date()
             if  last_act_out == today:
                 h.is_done_today = True
             h.sober_for = (today - last_act_out).days
             print("sober for:" + str(h.super_for))
    context = {
        'good_traits': good_traits,
        'bad_traits': bad_traits,
    }
    return render(request, 'index.html', context)

def checkin(request, id):
    today_checkins =  GoodTraitCheckIn.objects.filter(good_trait_id=id,  date__gte = datetime.today().date() )
    good_for = 0
    good_trait = GoodTrait.objects.get(pk=id)
    if not today_checkins:
        print("new checkin")
        good_for = good_trait.checkin()

    else:
        print("delete checkin")
        good_for = good_trait.rollback_checkin()

    print("good for:" + str(good_for))

    return JsonResponse({ 'goodFor': good_for })

def undo_checkin(request, id):
    GoodTraitCheckIn.objects.filter(date__gte=datetime.today().date(), good_trait_id = id).delete()
    good_trait = GoodTrait.objects.get(pk=id)
    good_trait.good_for = good_trait.good_for - 1
    good_trait.save()
    return HttpResponse(good_trait.good_for)

class GoodTraitCreate(CreateView):
    model = GoodTrait
    template_name  ="good_trait_form.html"
    # fields = ['name', 'image', 'description']
    form_class = GoodTraitForm
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(GoodTraitCreate, self).form_valid(form)
    def get_success_url(self):
        return "/"


def delete_good_trait(request, id):
    print("id" + str(id))
    GoodTrait.objects.filter(id = id).delete()
    return HttpResponse("Ok")

class BadTraitCreate(CreateView):
    model = BadTrait
    template_name  ="bad_trait_form.html"
    # fields = ['name', 'image', 'description']
    form_class = BadTraitForm
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(BadTraitCreate, self).form_valid(form)
    def get_success_url(self):
        return "/"

def delete_bad_trait(request, id):
    print("id" + str(id))
    BadTrait.objects.filter(id = id).delete()
    return HttpResponse("Ok")

def actout(request, id):
    today_actouts =  BadTraitActOut.objects.filter(bad_trait_id=id,  date__gte = datetime.today().date() )
    sober_for = 0
    bad_trait = BadTrait.objects.get(pk=id)
    if not today_actouts:
        print("new actout")
        sober_for = bad_trait.actout()
    else:
        print("delete checkin")
        sober_for = bad_trait.rollback_actout()

    print("sober for:" + str(sober_for))

    return JsonResponse({ 'soberFor': sober_for })

def undo_actout(request, id):
    GoodTraitCheckIn.objects.filter(date__gte=datetime.today().date(), good_trait_id = id).delete()
    good_trait = GoodTrait.objects.get(pk=id)
    good_trait.good_for = good_trait.good_for - 1
    good_trait.save()
    return HttpResponse(good_trait.good_for)
