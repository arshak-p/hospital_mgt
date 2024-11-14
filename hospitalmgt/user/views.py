from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('log_in')
    return render(request, 'login.html') 


# loginand authenticate
def admin_required(user):
    return user.role == 'Admin'

def receptionist_required(user):
    return user.role == 'Receptionist'

def billing_staff_required(user):
    return user.role == 'Billing Staff'


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)

            if user.role == 'Admin':
                return redirect(admin_dashboard)
            elif user.role == 'Receptionist':
                return redirect(receptionist_dashboard)
            elif user.role == 'Billing Staff':
                return redirect(billing_Staf_dashboard)

        else:
            messages.error(request, "Invalid username or password")
            return redirect("log_in")

    if request.user.is_authenticated:
        
        if request.user.role == 'Admin':
            return redirect(admin_dashboard)
        elif request.user.role == 'Receptionist':
            return redirect(receptionist_dashboard)
        elif request.user.role == 'Billing Staff':
            return redirect(billing_Staf_dashboard)

    return render(request, 'login.html')




def signout(request):
    logout(request)
    return HttpResponseRedirect("/")  

# admin

# role bsed users
@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request,"admin/admin_dashboard.html")


@login_required
@user_passes_test(receptionist_required)
def receptionist_dashboard(request):
    return render(request,"Receptionist/Receptionist_dashboard.html")


@login_required
@user_passes_test(billing_staff_required)
def billing_Staf_dashboard(request):
    return render(request,"Billing_Staf/Billing_Staf_dashboard.html")



User = get_user_model()


# createuser

@login_required
def create_user(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect(user_list) 
    else:
        form = CustomUserCreationForm()

    return render(request, 'admin/adduser.html', {'form': form})


# listing user

def user_list(request):
    users = User.objects.all()
    return render (request, 'admin/user_list.html', {'users':users})



# edituser



def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        role = request.POST.get('role')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        
        if current_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('edit_user', id=id)
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return redirect('edit_user', id=id)
            else:
                
                user.set_password(new_password)
        

        user.username = username
        user.role = role
        
        user.save()
       
        update_session_auth_hash(request, user)
        
        messages.success(request, 'User details updated successfully.')
        return redirect(user_list)
    
    return render(request, 'admin/edit_user.html', {'user': user})




# deleteuser
@login_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')

    
    user_to_delete.delete()
    messages.success(request, f"User '{user_to_delete.username}' has been deleted successfully.")
    return redirect('user_list')





# doctor


# Function to list all doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    print(doctors)
    return render(request, 'admin/doctor_list.html', {'doctors': doctors})

# Function to add a new doctor
def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        specialty = request.POST['specialty']
        availability = request.POST['availability']
        
        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            specialty=specialty,
            availability=availability

        ).save()
        
        messages.success(request, 'Doctor profile added successfully.')
        return redirect(doctor_list)
    return render(request, 'admin/add_doctor.html')

# Function to edit doctor details
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.first_name = request.POST['first_name']
        doctor.last_name = request.POST['last_name']
        doctor.specialty = request.POST['specialty']
        doctor.availability = request.POST['availability']
        doctor.save()
        messages.success(request, 'Doctor details updated successfully.')
        return redirect(doctor_list)
    return render(request, 'admin/edit_doctor.html', {'doctor': doctor})

# Function to delete doctor profile
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, f"Doctor {doctor.first_name} {doctor.last_name} deleted successfully.")
        return redirect(doctor_list)
    return redirect(doctor_list)

# Function to retrieve doctor details
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})






# BillingRecord



def add_billing_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        payment_date = request.POST['payment_date']
        remarks = request.POST.get('remarks', '')

        billing_record = BillingRecord.objects.create(
            patient=patient,
            amount=amount,
            payment_date=datetime.strptime(payment_date, '%Y-%m-%d').date(),
            remarks=remarks
        )
        messages.success(request, 'Billing record added successfully.')
        return redirect('patient_billing_history', patient_id=patient.id)
    return render(request, 'billing/add_billing_record.html', {'patient': patient})

def update_billing_record(request, billing_record_id):
    billing_record = get_object_or_404(BillingRecord, id=billing_record_id)
    if request.method == 'POST':
        billing_record.amount = request.POST.get('amount', billing_record.amount)
        payment_date = request.POST.get('payment_date')
        if payment_date:
            billing_record.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
        billing_record.remarks = request.POST.get('remarks', billing_record.remarks)
        billing_record.save()
        messages.success(request, 'Billing record updated successfully.')
        return redirect('patient_billing_history', patient_id=billing_record.patient.id)
    return render(request, 'billing/update_billing_record.html', {'billing_record': billing_record})

def delete_billing_record(request, billing_record_id):
    billing_record = get_object_or_404(BillingRecord, id=billing_record_id)
    if request.method == 'POST':
        billing_record.delete()
        messages.success(request, f'Billing record for {billing_record.patient} deleted successfully.')
        return redirect('patient_billing_history', patient_id=billing_record.patient.id)
    return render(request, 'billing/confirm_delete_billing_record.html', {'billing_record': billing_record})

def get_patient_billing_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    billing_records = BillingRecord.objects.filter(patient=patient).order_by('-payment_date')
    return render(request, 'billing/patient_billing_history.html', {'patient': patient, 'billing_records': billing_records})

def search_billing_records(request):
    patient_id = request.GET.get('patient_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    billing_records = BillingRecord.objects.all()
    if patient_id:
        billing_records = billing_records.filter(patient_id=patient_id)
    if start_date:
        billing_records = billing_records.filter(payment_date__gte=start_date)
    if end_date:
        billing_records = billing_records.filter(payment_date__lte=end_date)

    return render(request, 'billing/search_billing_records.html', {'billing_records': billing_records})






