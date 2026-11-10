# Exo 2 - ABCD Records

## Level 1 - Task 1.1: basic use case diagram

The boxes and arrows show the actors and their actions. This is a simple use case view made with Mermaid.

```mermaid
flowchart LR
    M[Member]
    C[Order Processing Clerk]
    subgraph SYS[ABCD Records System]
        P([Place Order])
        V([Verify Membership])
        O([Process Order])
        Y([Make Payment])
    end
    M --- P
    M --- Y
    C --- V
    C --- O
```

## Level 1 - Task 1.2: basic class diagram

```mermaid
classDiagram
    class Member {
        +int member_id
        +str name
        +str address
        +str member_type
        +place_order()
        +make_payment()
    }
    class Order {
        +int order_id
        +str date
        +float total
        +str status
        +calculate_total()
        +confirm()
    }
    class OrderProcessingClerk {
        +int clerk_id
        +str name
        +str department
        +str shift
        +verify_membership()
        +process_order()
    }
    Member "1" -- "0..*" Order : places
    OrderProcessingClerk "1" -- "0..*" Order : processes
```

## Level 2 - Task 2.1: complete use case diagram

Mermaid does not have a native UML use case diagram type, so this flowchart uses a system boundary, actor boxes, and labelled `«include»` / `«extend»` relations. It is a readable approximation rather than a formal UML use case drawing.

```mermaid
flowchart LR
    M[Member]
    R[Royal Member]
    N[Non-Member]
    OC[Order Processing Clerk]
    CC[Collection Department Clerk]
    subgraph SYS[ABCD Records System]
        PO([Place Order])
        VM([Verify Membership])
        VI([Verify Item Availability])
        AD([Apply Discount])
        PI([Print Invoice])
        PS([Print Shipping List])
        OU([Order Unavailable Items])
        MA([Send Membership Application])
        MP([Make Payment])
        PR([Process Order])
    end
    M --- PO
    M --- MP
    R --- OU
    N --- MA
    R -.->|specializes| M
    OC --- PR
    OC --- VM
    CC --- MP
    PO -.->|«include»| VM
    PR -.->|«include»| VI
    PR -.->|«include»| PI
    PR -.->|«include»| PS
    AD -.->|«extend»: Royal member| PR
    OU -.->|«extend»: Royal and unavailable| PR
    MA -.->|«extend»: Not a member| VM
```

## Level 2 - Task 2.2: complete class diagram

`RoyalMember` and `RegularMember` inherit from `Member`. Different payment methods inherit from `Payment`. CDs and tapes inherit from `Item`. An order owns its order lines.

```mermaid
classDiagram
    class Member {
        +int id
        +str name
        +str address
        +place_order()
    }
    class RoyalMember {
        +float discount
        +bool priority
        +order_unavailable()
    }
    class RegularMember {
        +place_order()
    }
    class Order {
        +int id
        +str status
        +float total
        +calculate_total()
    }
    class OrderLine {
        +int quantity
        +float unit_price
        +line_total()
    }
    class Item {
        +str title
        +float price
        +int stock
        +is_available()
    }
    class CD {
        +str artist
    }
    class Tape {
        +str artist
    }
    class Invoice {
        +int id
        +float total
        +print_invoice()
    }
    class ShippingList {
        +int id
        +str address
        +print_list()
    }
    class Payment {
        <<abstract>>
        +float amount
        +process()
    }
    class Cash {
        +process()
    }
    class Check {
        +process()
    }
    class BankDraft {
        +process()
    }
    class MembershipApplication {
        +str applicant_name
        +str status
        +send_form()
    }
    class OrderProcessingClerk {
        +int id
        +verify_membership()
        +process_order()
    }
    class CollectionDepartmentClerk {
        +int id
        +collect_payment()
    }
    Member <|-- RoyalMember
    Member <|-- RegularMember
    Item <|-- CD
    Item <|-- Tape
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft
    Member "1" -- "0..*" Order : places
    Member "1" -- "0..*" MembershipApplication : applications
    Order "1" *-- "1..*" OrderLine : contains
    OrderLine "0..*" --> "1" Item : refers to
    Order "1" *-- "1" Invoice : produces
    Order "1" *-- "1" ShippingList : produces
    Order "1" -- "0..1" Payment : paid by
    OrderProcessingClerk "1" -- "0..*" Order : processes
    CollectionDepartmentClerk "1" -- "0..*" Payment : collects
```

## Level 2 - Example: Royal member orders two CDs

A Royal member orders two CDs. One is in stock and the other is not. The system accepts the unavailable CD because this member is Royal. The clerk applies the Royal discount, prepares an invoice, and accepts a check payment.

## Level 3 - Sequence 1: complete order processing

```mermaid
sequenceDiagram
    actor Member
    participant System
    participant OrderClerk
    participant Inventory
    participant CollectionClerk
    participant DailyRecords
    Member->>System: Place order
    System->>OrderClerk: Review order
    OrderClerk->>System: Verify membership
    System->>Inventory: Check item stock
    Inventory-->>System: Availability
    alt All available or Royal member
        System->>System: Apply Royal discount if needed
        System->>System: Create invoice and shipping list
        Member->>CollectionClerk: Make payment
        CollectionClerk-->>System: Confirm payment
        System->>DailyRecords: Save order
        System-->>Member: Confirm order
    else Unavailable and Regular member
        System-->>Member: Order cannot be completed
    end
```

## Level 3 - Sequence 2: membership verification

```mermaid
sequenceDiagram
    actor Customer
    participant OrderClerk
    participant System
    Customer->>OrderClerk: Request an order
    OrderClerk->>System: Verify membership
    alt Valid member
        System-->>OrderClerk: Member confirmed
        OrderClerk-->>Customer: Continue with order
    else Not a member
        System-->>OrderClerk: No membership found
        OrderClerk-->>Customer: Send membership application
    end
```

## Level 3 - Sequence 3: payment processing

```mermaid
sequenceDiagram
    actor Member
    participant CollectionClerk
    participant Payment
    participant System
    Member->>CollectionClerk: Choose payment method
    alt Cash
        CollectionClerk->>Payment: process cash
    else Check
        CollectionClerk->>Payment: process check
    else Bank Draft
        CollectionClerk->>Payment: process bank draft
    end
    Payment-->>CollectionClerk: Success or failure
    alt Success
        CollectionClerk->>System: Save payment and update order
        System-->>Member: Payment confirmed
    else Failure
        CollectionClerk-->>Member: Payment failed
    end
```

## Level 3 - Sequence 4: reorder unavailable item for Royal member

```mermaid
sequenceDiagram
    actor RoyalMember
    participant OrderClerk
    participant Inventory
    participant Supplier
    participant System
    RoyalMember->>OrderClerk: Order unavailable CD
    OrderClerk->>System: Check Royal membership
    System-->>OrderClerk: Royal confirmed
    OrderClerk->>Inventory: Check stock
    Inventory-->>OrderClerk: Out of stock
    OrderClerk->>Supplier: Request CD reorder
    Supplier-->>OrderClerk: Reorder accepted
    OrderClerk->>System: Save pending item in order
    System-->>RoyalMember: Order accepted, item pending
```
