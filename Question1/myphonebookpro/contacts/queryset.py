from .models import Contact


def contact_list_query():
    contacts = Contact.objects.all()
    return contacts


def add_contact_query(firstname, lastname, phone, address):
    pass
