import json
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .models import Contact
from django.http import HttpResponse, request
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if not first_name or not last_name or not phone:
            return HttpResponse("Missing required parameters", status=400)

        if Contact.objects.filter(phone=phone).exists():
            return HttpResponse("This phone number is already in use.", status=400)

        contact = Contact(first_name=first_name, last_name=last_name, phone=phone, address=address)
        contact.save()
        return HttpResponse("Contact added successfully", status=201)
    else:
        return HttpResponse("Invalid request method", status=405)


@csrf_exempt
def delete_contact(request):
    if request.method == 'DELETE':
        name = request.GET.get('name')

        if not name:
            return HttpResponse("Name parameter is missing", status=400)

        contact = Contact.objects.filter(Q(first_name=name) | Q(last_name=name)).first()

        if contact:
            contact.delete()
            return redirect('contact_list')
        else:
            message = f"No contact found with the name '{name}'."
            return HttpResponse(message, status=404)
    else:
        return HttpResponse("Invalid request method", status=405)


#
def contact_list(request):
    contacts = Contact.objects.all()
    contact_data = [
        {'first_name': contact.first_name, 'last_name': contact.last_name, 'phone': str(contact.phone),
         'address': contact.address} for contact in contacts]
    return HttpResponse(json.dumps(contact_data), content_type='application/json')

def search_contact(request):
    query = request.GET.get('q')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    contact_list = [{'first_name': contact.first_name, 'last_name': contact.last_name, 'phone': str(contact.phone),
                     'address': contact.address} for contact in contacts]
    return HttpResponse(json.dumps(contact_list), content_type='application/json')
