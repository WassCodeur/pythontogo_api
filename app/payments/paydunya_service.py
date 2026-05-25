import paydunya
from paydunya import InvoiceItem, Store, Invoice
from app.core.settings import settings, infos


paydunya.debug = settings.debug

paydunya.api_keys = {
    "PAYDUNYA-MASTER-KEY": settings.paydunya_master_key,
    "PAYDUNYA-PRIVATE-KEY": settings.paydunya_private_key,
    "PAYDUNYA-TOKEN": settings.paydunya_token,
}

store = Store(**infos)

base_url = settings.base_url.rstrip("/")


def create_invoice(description, unit_price, callback_url=None,   qte=1, name=None, success_page_url=None, cancel_page_url=None):
    if unit_price < 200:
        raise ValueError("Unit price must be greater or equal to 200")
    if qte < 1:
        raise ValueError("Quantity must be greater or equal to 1")
    total_price = unit_price * qte
    invoice = Invoice(
        store=store
    )

    items = [
        InvoiceItem(
            name=name,
            quantity=qte,
            unit_price=unit_price,
            total_price=total_price,
            description=description
        )
    ]

    invoice.add_items(items)
    invoice.calculate_total_amt()
    invoice.cancel_url = cancel_page_url or f"{base_url}/checkout/payment/cancel"
    invoice.return_url = success_page_url or f"{base_url}/checkout/payment/success"
    if callback_url and callback_url.startswith("https://"):
        invoice.callback_url = callback_url

    successful, response = invoice.create()
    if successful:
        return response.get("response_text")
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
