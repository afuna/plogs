from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.dispatch import Signal
from .models import Plane, Engine, Prop
from .forms import SimplePlaneForm
from .signals import post_create

@login_required
def new(request):
    if request.method == "POST":
        form = SimplePlaneForm(request.POST)
        if form.is_valid():
            engine = Engine()
            engine.save()

            prop = Prop()
            prop.save()

            plane = Plane(owner=request.user,
                          kit = form.save(),
                          engine = engine,
                          prop = prop)
            plane.save()

            post_create.send(sender=Plane, plane=plane)

            return redirect('frontpage')
    else:
        form = SimplePlaneForm()

    context = {
        'form': form,
        'form_url': reverse_lazy('planes:new'),
        'form_button': 'Start Logging',
        'title': 'Add Your Plane Kit',
    }
    return render(request, 'base_form.html', context)
