# Exo 1 - Hospital Management System

## Task 1 - Basic class diagram

The three main roles are Patient, Doctor, and Organizer. The organizer connects patients and doctors.

```mermaid
classDiagram
    class Patient {
        +int id
        +str name
        +str password
        +str email
        +submit_problem(text)
        +view_prescription()
        +pay(amount)
    }
    class Doctor {
        +int id
        +str name
        +str password
        +str specialty
        +review_problem(problem)
        +write_prescription(problem)
    }
    class Organizer {
        +int id
        +str name
        +str password
        +str role
        +send_to_doctor(problem)
        +send_prescription(patient)
        +manage_members()
    }
    Patient "0..*" -- "1" Organizer : contacts
    Organizer "0..*" -- "0..*" Doctor : consults
```

## Task 2 - Full class diagram

The design has the six requested classes. The `PaymentType` enumeration stores the three payment methods. A patient can submit many health problems. One problem can have zero or one prescription in this simple version.

```mermaid
classDiagram
    class Patient {
        +int id
        +str name
        +submit_problem(text)
        +make_payment(amount)
    }
    class Organizer {
        +int id
        +str name
        +assign_doctor(problem)
        +send_prescription(patient)
        +forward_payment(doctor)
    }
    class Doctor {
        +int id
        +str name
        +write_prescription(problem)
    }
    class HealthProblem {
        +int id
        +str description
        +str status
        +change_status(status)
    }
    class Prescription {
        +int id
        +str instructions
        +str created_at
    }
    class Payment {
        +int id
        +float amount
        +PaymentType type
        +str status
        +process()
    }
    class PaymentType {
        <<enumeration>>
        CASH
        CHECK
        CREDIT_CARD
    }
    Patient "1" *-- "0..*" HealthProblem : submits
    HealthProblem "1" *-- "0..1" Prescription : result
    Doctor "1" -- "0..*" Prescription : writes
    Organizer "1" -- "0..*" HealthProblem : manages
    Organizer "0..*" -- "0..*" Doctor : consults
    Patient "1" -- "0..*" Payment : makes
    Payment --> PaymentType : uses
    Organizer "1" -- "0..*" Payment : forwards
    Doctor "1" -- "0..*" Payment : receives
```

## Task 2 - Sequence diagram: consultation and payment

```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant Doctor
    Patient->>Organizer: Submit health problem
    Organizer->>Doctor: Ask for consultation
    Doctor-->>Organizer: Send prescription
    Organizer-->>Patient: Deliver prescription
    Patient->>Organizer: Pay (cash, check, or card)
    Organizer->>Doctor: Forward payment
    Doctor-->>Organizer: Confirm receipt
```

## Task 3 - Advanced class design

All people share basic information in the `User` superclass. A problem has a status and a creation time. A patient can see previous prescriptions. Payment types use different implementations of `process()`.

```mermaid
classDiagram
    class User {
        +int id
        +str name
        +str password
        +login()
        +logout()
    }
    class Patient {
        +str email
        +submit_problem(text)
        +view_history()
    }
    class Doctor {
        +str specialty
        +write_prescription(problem)
    }
    class Organizer {
        +bool is_admin
        +register_patient()
        +update_database()
        +forward_payment()
    }
    class HealthProblem {
        +int id
        +str description
        +str status
        +datetime created_at
        +update_status()
    }
    class Prescription {
        +int id
        +str instructions
        +datetime created_at
    }
    class Payment {
        <<abstract>>
        +float amount
        +str status
        +process()
    }
    class CashPayment {
        +process()
    }
    class CheckPayment {
        +process()
    }
    class CreditCardPayment {
        +process()
    }
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Payment <|-- CashPayment
    Payment <|-- CheckPayment
    Payment <|-- CreditCardPayment
    Patient "1" -- "0..*" HealthProblem : submits
    HealthProblem "1" -- "0..*" Prescription : history
    Doctor "1" -- "0..*" Prescription : writes
    Organizer "1" -- "0..*" HealthProblem : manages
    Organizer "0..*" -- "0..*" Doctor : consults
    Patient "1" -- "0..*" Payment : makes
    Payment "0..*" --> "1" Doctor : paid to
```

## Task 3 - Sequence 1: patient registration

```mermaid
sequenceDiagram
    actor Patient
    participant Organizer
    participant System
    participant Database
    Patient->>Organizer: Ask to register
    Organizer->>System: Create member details
    System->>Database: Save patient
    Database-->>System: New patient ID
    System-->>Organizer: Confirm registration
    Organizer-->>Patient: Send ID and login details
```

## Task 3 - Sequence 2: consultation flow

```mermaid
sequenceDiagram
    actor Patient
    participant System
    participant Organizer
    participant Doctor
    Patient->>System: Submit health problem
    System->>System: Set status = pending
    System->>Organizer: Notify new problem
    Organizer->>Doctor: Share problem
    System->>System: Set status = in-review
    Doctor-->>Organizer: Provide prescription
    Organizer->>System: Save prescription and timestamp
    System->>System: Set status = resolved
    System-->>Patient: Show prescription
```

## Task 3 - Sequence 3: payment processing

```mermaid
sequenceDiagram
    actor Patient
    participant System
    participant PaymentMethod
    participant Organizer
    participant Doctor
    Patient->>System: Choose payment type and pay
    System->>PaymentMethod: process(amount)
    alt Payment accepted
        PaymentMethod-->>System: Success
        System->>System: Save payment record
        System->>Organizer: Notify payment received
        Organizer->>Doctor: Forward payment
        Doctor-->>Organizer: Confirm receipt
        Organizer->>System: Mark payment as forwarded
        System-->>Patient: Payment confirmed
    else Payment rejected
        PaymentMethod-->>System: Failed
        System-->>Patient: Show payment error
    end
```
