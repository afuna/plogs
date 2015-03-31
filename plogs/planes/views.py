from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plane, Engine, Prop
from .forms import SimplePlaneForm

from plogs.buildlogs.models import Project

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

            # FIXME: this is not the best place to do this, but it'll do for now
            project = Project(plane=plane)
            project.save()

            return redirect('frontpage')
    else:
        form = SimplePlaneForm()

    context = {
        'form': form,
        'form_url': 'planes:new',
        'form_button': 'Start Logging',
        'title': 'Add Your Plane Kit',
    }
    return render(request, 'base_form.html', context)
