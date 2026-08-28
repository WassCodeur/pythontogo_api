import csv
import time
import requests

from app.core.settings import settings

headers = {
    "Authorization": f"Bearer {settings.whatsapp_token}",
    "Content-Type": "application/json",
}


TEMPLATE_NAME = "pycon_togo_2026_commence_aujourdhui_"


def send_whatsapp_message(to, template_name, language_code: str, components: list = None):
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
        }
    }

    if components:
        data["template"]["components"] = components

    r = requests.post(settings.whatsapp_api_url,
                      headers=headers, json=data, timeout=30)
    return r.status_code, r.json()


# antendees_sheets/pycontg25_attendees_pycontg25_attendees.csv
# antendees_sheets/pycontg25_attendees_registrations_rows.csv
# antendees_sheets/pycontg25_attendees_registrations_rows_2.csv
# antendees_sheets/pycontg25_attendees_registrations_rows_3.csv

CONTACTS_FILE = "antendees_sheets/merge-csv.com__6a90ddd656972.csv"
# "antendees_sheets/pycontg25_attendees_Sheet1.csv"


def send_template(numero):
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,  # format: 22890123456 sans + ni espace
        "type": "template",
        "template": {
            "name": TEMPLATE_NAME,
            "language": {"code": "fr"},

        }
    }
    r = requests.post(settings.whatsapp_api_url,
                      headers=headers, json=payload)
    return r.status_code, r.json()


if __name__ == "__main__":
    with open(CONTACTS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            # Prendre le premier mot comme prénom
            prenom = row['name'].strip().split()[0]
            numero = row['phone_number'].strip()

            # if not numero.startswith("228"):
            #    print(f"Skip {numero} - format invalide")
            #    continue

            status, result = send_template(numero)
            print(f"{count + 1}- [{status}] {prenom} -> {result}")
            # print(f"{count + 1}-{prenom} -> {numero}")

            # Anti-ban obligatoire
            time.sleep(5)  # 5 secondes entre chaque envoi

            count += 1
            if count % 40 == 0:
                print(f"{count} envoyés - pause 5 min...")
                time.sleep(300)

    print("Terminé.")
