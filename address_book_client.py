import address_book_pb2

_TIMEOUT_SECONDS = 10


def prompt_for_address(contact):
    contact.id = int(raw_input("Enter person ID number: "))
    contact.name = raw_input("Enter name: ")

    email = raw_input("Enter email address (blank for none): ")
    if email != "":
        contact.email = email

    while True:
        number = raw_input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = contact.phone.add()
        phone_number.number = number

        type = raw_input("Is this a mobile, home, or work phone? ")

        if type == "mobile":
            phone_number.type = address_book_pb2.Person.MOBILE
        elif type == "home":
            phone_number.type = address_book_pb2.Person.HOME
        elif type == "work":
            phone_number.type = address_book_pb2.Person.WORK
        else:
            print "Unknown phone type; leaving as default value."

    return contact


def prompt_for_search_string():
    search_string = raw_input("Enter name of contact to find:\n")
    if search_string != "":
        return search_string

    return ''


def print_menu():
    print "Enter your choice: \n1 : Add New Address\n2 : Search Addresses\n3 : List all addresses\n4: Exit Address Book"

def print_contact(contact):
    print "\n--------------------------------------"
    print "ID: ", contact.id
    print "Name: ", contact.name
    if contact.email is not None:
        print "Email: ", contact.email
    phone_number_count = 0
    for phone_number in contact.phone:
        phone_number_count += 1
        print "Phone ", phone_number_count
        print "Type ", phone_number.type
        print "Number ", phone_number.number

    print "--------------------------------------\n"




def add_address(server_stub):
    contact = address_book_pb2.Person()
    contact = prompt_for_address(contact)

    response = server_stub.AddAddress(contact, _TIMEOUT_SECONDS)
    print "Address Book Client client received: " + response.message


def search_addresses(server_stub):
    search_request = address_book_pb2.SearchRequest(search_string=prompt_for_search_string())

    response = server_stub.SearchAddresses(search_request, _TIMEOUT_SECONDS)
    print "results matching search string %s are", search_request.search_string

    for contact in response.results:
        print_contact(contact)


def list_all_addresses(server_stub):
    all_request = address_book_pb2.SearchRequest(search_string='')
    response = server_stub.AllAddresses(all_request, _TIMEOUT_SECONDS)

    print "returned all addresses"
    for contact in response.contacts:
        print_contact(contact)


def run():
    with address_book_pb2.early_adopter_create_AddressBookService_stub('localhost', 50051) as stub:
        while True:
            print_menu()
            choice = int(raw_input(": "))
            if choice == 1:
                add_address(stub)
            elif choice == 2:
                search_addresses(stub)
            elif choice == 3:
                list_all_addresses(stub)
            elif choice == 4:
                print "Bye Bye!"
                exit(9)
            else:
                print 'invalid choice, try again'


if __name__ == '__main__':
    run()