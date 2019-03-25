from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import Item, List
from django.contrib.auth import get_user_model
User = get_user_model()

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

# # don't enter this code yet, we're only imagining it
#
# def new_list(request):
#     form = NewListForm(data=request.POST)
#     if form.is_valid():
#         list_ = form.save(owner=request.user)  # creates both List and Item
#         return redirect(list_)
#     else:
#         return render(request, 'home.html', {"form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

def new_list2(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
