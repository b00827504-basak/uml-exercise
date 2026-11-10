# Hospital Management System - Design Questions

## 1. How would you handle a patient consulting multiple doctors?

A patient can be linked to more than one doctor through a health problem. Each doctor can give a different prescription or opinion. The system should save which doctor wrote each prescription.

## 2. Should prescriptions be reusable? How would you model that?

I would keep old prescriptions in the patient's history, but I would not automatically reuse them. Each prescription has its own ID, date, doctor, and health problem. A doctor can look at older prescriptions before writing a new one.

## 3. What design pattern fits the payment system?

The Strategy pattern is a good choice. Cash, check, and credit card payments have the same `process()` method, but they can work differently.

## 4. How do you ensure data integrity when payments are processed?

The system should check the amount and payment status before saving. Each payment should have a unique ID. It should record a payment only once and keep a history of updates. If a payment fails, it should not be marked as paid.

## Note

This is a simple UML and Python exercise. A real hospital system would also need security, privacy protection, and secure payment services.
