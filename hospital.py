"""A small example based on the hospital UML diagrams."""
from datetime import datetime


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def login(self):
        return f"{self.name} logged in."

    def logout(self):
        return f"{self.name} logged out."


class Patient(User):
    def submit_problem(self, description):
        return HealthProblem(description)


class Doctor(User):
    def write_prescription(self, problem, instructions):
        problem.status = "resolved"
        return Prescription(instructions, self)


class Organizer(User):
    def consult_doctor(self, problem):
        problem.status = "in-review"

    def forward_payment(self, payment):
        if payment.status == "paid":
            payment.status = "forwarded"
            return True
        return False


class HealthProblem:
    def __init__(self, description):
        self.description = description
        self.status = "pending"
        self.created_at = datetime.now()
        self.prescriptions = []


class Prescription:
    def __init__(self, instructions, doctor):
        self.instructions = instructions
        self.doctor = doctor
        self.created_at = datetime.now()


class Payment:
    def __init__(self, amount):
        self.amount = amount
        self.status = "pending"

    def process(self):
        raise NotImplementedError


class CashPayment(Payment):
    def process(self):
        self.status = "paid"
        return True


class CheckPayment(Payment):
    def process(self):
        self.status = "paid"
        return True


class CreditCardPayment(Payment):
    def process(self):
        self.status = "paid"
        return True


if __name__ == "__main__":
    patient = Patient(1, "Alex")
    doctor = Doctor(2, "Dr. Lee")
    organizer = Organizer(3, "Sam")

    problem = patient.submit_problem("I have a headache.")
    print("Problem status:", problem.status)
    organizer.consult_doctor(problem)
    prescription = doctor.write_prescription(problem, "Rest and drink water.")
    problem.prescriptions.append(prescription)
    print("Doctor's advice:", prescription.instructions)
    print("Problem status:", problem.status)

    payment = CashPayment(20)
    payment.process()
    organizer.forward_payment(payment)
    print("Payment status:", payment.status)
