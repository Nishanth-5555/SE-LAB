# Lab 3 - Component Modelling & Architectural Pattern Selection

**Scenario:** Self-Service Coffee Kiosk System
**Chosen architecture:** Layered (Presentation -> Business Logic -> Data / Hardware)

## Deliverables
| File | Description |
|------|-------------|
| `Component_Diagram.png` / `Component_Diagram.pdf` | UML component diagram |
| `Lab3_Architecture_Justification.docx` / `.pdf` | One-page written justification |

## Components (8)
Touch Screen UI, Order Manager, Menu & Pricing Service, Payment Service, Receipt Service, Menu Database, Card Reader (device), Receipt Printer (device)

## Interfaces (8, ball = provided / socket = required)
| Interface | Provided by | Required by | Technology |
|-----------|-------------|-------------|------------|
| IOrder | Order Manager | Touch Screen UI | API call |
| IMenu | Menu & Pricing Service | Touch Screen UI | API call |
| IPricing | Menu & Pricing Service | Order Manager | API call |
| IPayment | Payment Service | Order Manager | API call |
| IReceipt | Receipt Service | Order Manager | API call |
| IMenuData | Menu Database | Menu & Pricing Service | SQL query |
| ICardReader | Card Reader | Payment Service | USB / EMV hardware API |
| IPrinter | Receipt Printer | Receipt Service | USB / ESC-POS |
