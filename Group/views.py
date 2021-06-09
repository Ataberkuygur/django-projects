from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm

@login_required(login_url='User:login')
def GroupCreate(request):
    if request.user.score > 100:
        form = GroupForm()
        if request.method == "POST":
            form = GroupForm(request.POST or None)
            if form.is_valid():
                group = form.save(commit=False)
                slug = group.slug
                group.save()
                return redirect('Group:detail', kwargs={'slug': slug})
            else:
                return render(request, 'group/create.html', {'form': form})
        else:
            return render(request, 'group/create.html', {'form': form})
    else:
        return HttpResponse('100 puana sahip olmalısınız!')

@login_required(login_url='User:login')
def GroupDetail(request, slug):
    group = Group.objects.get(slug=slug)
    return render(request, 'group/detail.html', {'group': group})

