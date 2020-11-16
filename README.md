# SafeEntry-Web-App
A flask web application for the logging of student's entry and exit into various school facilities such as the library, computer labs or lounges.


# Check-In page:
The check-in page has an address of "/checkin/(location id)/(seat no.)". To access this page, schools will paste QR codes on the various tables in the spaces
which they want to log entry and exit of. For example, Library seat number 1 will have a QR code that when scanned redirects users to the web app, with the
address "/checkin/LIB/1". This then asks for their Matric Number, a unique identifiable string for each student. Students input their matric number and are
then able to successfully "Check In" or book the seat.

# Check-Out page:
This page is automatically shown after users successfully "Check-In". Users are encouraged to keep this tab open, in order to check out from the seat later on.
It will consist of one button when clicked will successfully check out that user from the seat. The address of this page will be "/checkout/(unique sha256 string)".
A sha256 encryption algorithm is used to obsfucate the checkout addresses to prevent malicious users from checking out on other's behalf. Each check-out page is unique
for each check-in page, and will not work if the seat in the specific location is not checked in. e.g check-out page for seat no. 1 in Library will not work if
seat no. 1 in Library has not been checked-in.

# Admin page:
This page allows admins to view ALL entries and exits for ALL venues at ALL times. This page has address "/admin/entries/" and allows administrators to filter by 
MatricNo, Name, Class, Gender, Seat Number, Location. It allows for easy logging and access to data, as well as easy access to student's names and pandemic tracking
purposes.
