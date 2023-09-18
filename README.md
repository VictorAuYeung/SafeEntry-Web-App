# SafeEntry-Web-App
This project was created using Flask and Python.
This application contains only the HTML and code logic component for the logging of student's entry and exit into various school facilities such as the library, computer labs or lounges.
Additional CSS and design elements are not included for copyright issues.


# Check-In page:
The check-in page has an address of "/checkin/(location id)/(seat no.)". To access this page, schools will paste QR codes on the various tables in the spaces
which they want to log entry and exit of. For example, Library seat number 1 will have a QR code that when scanned redirects users to the web app, with the
address "/checkin/LIB/1". This then asks for their Matric Number, a unique identifiable string for each student. Students input their matric number and are
then able to successfully "Check In" or book the seat.

![image](https://github.com/VictorAuYeung/SafeEntry-Web-App/assets/69711600/a5cb541d-9e25-4f3c-bba9-dd73e09adc19)


# Check-Out page:
This page is automatically shown after users successfully "Check-In". Users are encouraged to keep this tab open, in order to check out from the seat later on.
It will consist of one button when clicked will successfully check out that user from the seat. The address of this page will be "/checkout/(unique sha256 string)".
A sha256 encryption algorithm is used to obsfucate the checkout addresses to prevent malicious users from checking out on other's behalf. Each check-out page is unique
for each check-in page, and will not work if the seat in the specific location is not checked in. e.g check-out page for seat no. 1 in Library will not work if
seat no. 1 in Library has not been checked-in.

![image](https://github.com/VictorAuYeung/SafeEntry-Web-App/assets/69711600/9e2a831b-0690-46b2-8e58-8864922024a8)


# Admin page:
This page allows admins to view ALL entries and exits for ALL venues at ALL times. This page has address "/admin/entries/" and allows administrators to filter by 
MatricNo, Name, Class, Gender, Seat Number, Location. It allows for easy logging and access to data, as well as easy access to student's names and pandemic tracking
purposes.

![image](https://github.com/VictorAuYeung/SafeEntry-Web-App/assets/69711600/506663ff-01e4-4964-ab97-80bc9e30e40a)

