from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plane, Engine, Prop
from .forms import SimplePlaneForm

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
