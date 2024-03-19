

from django.shortcuts import render, redirect
from django.contrib.auth import  login
from .forms import  MedicineForm
from .models import Medicine
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login 
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html')


#signup
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            # Redirect to login page after successful signup
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

#login

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            # Redirect to home page after successful login
            return redirect('medicines_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#medicine listing/search

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url = '/login/')
def medicines_list(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
       
        medicines = Medicine.objects.filter(name__istartswith=search_query) 
                    
    else:
        
        medicines = Medicine.objects.all()

    return render(request, 'medicines_list.html', {'medicines': medicines, 'search_query': search_query})


#Add

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_medicine(request, medicine_id=None):
    if medicine_id:
        medicine = get_object_or_404(Medicine, id=medicine_id)
    else:
        medicine = None

    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicines_list')
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'add_medicine.html', {'form': form, 'medicine': medicine})



# edit

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicines_list')
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'edit_medicine.html', {'form': form, 'medicine': medicine})


# Delete
from django.shortcuts import get_object_or_404

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if request.method == 'POST':
        # Perform the deletion
        medicine.delete()
        return redirect('medicines_list')

    return render(request, 'medicines_list.html', {'medicines': Medicine.objects.all()})




#Logout

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect('login')



