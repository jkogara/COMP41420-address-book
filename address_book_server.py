import time

import address_book_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class AddressBookService(address_book_pb2.EarlyAdopterAddressBookServiceServicer):

    remote_address_book = address_book_pb2.AddressBook()

    def AddAddress(self, request, context):
        AddressBookService.remote_address_book.contacts.extend([request])

        return address_book_pb2.AddAddressReply(message='%s was added to the address book' % request.name)

    def AllAddresses(self, request, context):
        return address_book_pb2.AddressBook(contacts=AddressBookService.remote_address_book.contacts)

    def SearchAddresses(self, request, context):
        results = []

        for contact in AddressBookService.remote_address_book.contacts:
            if request.search_string.lower() in contact.name.lower():
                results.append(contact)

        return address_book_pb2.SearchResult(results=results)


def serve():
    server = address_book_pb2.early_adopter_create_AddressBookService_server(
        AddressBookService(), 50051, None, None)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    serve()