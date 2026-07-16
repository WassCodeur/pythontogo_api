import paydunya
from paydunya import InvoiceItem, Store, Invoice
from app.core.settings import settings, infos
from app.schemas.payment import Payment


paydunya.debug = settings.debug

paydunya.api_keys = {
    "PAYDUNYA-MASTER-KEY": settings.paydunya_master_key,
    "PAYDUNYA-PRIVATE-KEY": settings.paydunya_private_key,
    "PAYDUNYA-TOKEN": settings.paydunya_token,
}

store = Store(**infos)

base_url = settings.base_url.rstrip("/")
root_path = settings.root_path.rstrip("/").lstrip("/")
base_url = f"{base_url}/{root_path}" if root_path else base_url


def create_invoice(payment: Payment):
    payment = Payment(**payment)
    if payment.unit_price < 200:
        raise ValueError("Unit price must be greater or equal to 200")
    if payment.quantity < 1:
        raise ValueError("Quantity must be greater or equal to 1")
    total_price = payment.unit_price * payment.quantity
    invoice = Invoice(
        store=store
    )

    items = [
        InvoiceItem(
            name=payment.name,
            quantity=payment.quantity,
            unit_price=payment.unit_price,
            total_price=total_price,
            description=payment.description
        )
    ]

    invoice.add_items(items)
    invoice.calculate_total_amt()
    invoice.cancel_url = payment.cancel_page_url or f"{base_url}/checkout/payment/cancel"
    invoice.return_url = payment.success_page_url or f"{base_url}/checkout/payment/success"
    if payment.callback_url and payment.callback_url.startswith("https://"):
        invoice.callback_url = payment.callback_url

    successful, response = invoice.create()
    if successful:
        return {"payment_url": response.get("response_text")}
    else:
        raise Exception("Failed to create invoice")


if __name__ == "__main__":
    try:
        url = create_invoice(
            description="Test Invoice",
            callback_url="https://example.com/callback",
            unit_price=5000,
            qte=2,
            name="Test Product"
        )
        print("Invoice URL:", url)
    except Exception as e:
        print("Error creating invoice:", str(e))
