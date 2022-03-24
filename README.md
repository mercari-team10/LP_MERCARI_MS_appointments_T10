# Appointments Microservice

The Appointments microservice deals with the process of booking and modifying appointments for the doctors and the labs. The appointment microservice interacts with the calendar microservice in order to provide a full in-sync scenario to the patients as well as to the doctors. When a patient tries to book an appointment with a doctor, he/she provides a start time and duration of the consultation. This request is then routed to the appointments microservice, which further routes it to the calendar microservice, and checks if the slot is available or not. If yes, the patient then books an appointment, and the corresponding entries are made to the calendar database as well as to the appointment database. The microservice uses PostgreSQL as the database.

The various endpoints contained in this microservice include the following:

- `/doc_appnt [METHOD = POST]` : This endpoint is used to insert an event into the schedule of the doctor.

- `/doc_appnt [METHOD = GET` : This endpoint is used to extract the appointments of a particular doctor, corresponding to a patient

- `/doc_appnt [METHOD = DELETE]` : This endpoint is used to delete a particular the appointment of a doctor corresponding to a given appointment id

- `/doc_appnt_single` : This endpoint is used to retrieve all the appointments of a particular doctor.

- `/lab_appnt [METHOD = GET]` : This endpoint is used to get the details corresponding to a particular `test_id` and `patient_id`

- `/lab_appnt [METHOD = DELETE]` : This endpoint is used to remove a particular lab appointment of a patient.

- `/check_availability` : This endpoint acts as the middleman between the frontend and the Calendar microservice.



