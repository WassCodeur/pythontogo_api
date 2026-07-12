hmlt_template = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Template</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #f4f6f8;
      font-family: Arial, sans-serif;
    }

    .container {
      width: 100%;
      padding: 20px 0;
      display: flex;
      justify-content: center;
    }

    .email-card {
      width: 100%;
      max-width: 600px;
      background: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .header {
      padding: 20px;
      text-align: center;
      color: #ffffff;
      font-size: 20px;
      font-weight: bold;
    }

    .content {
      padding: 25px;
      color: #333333;
      line-height: 1.6;
      font-size: 15px;
    }

    .content h1 {
      font-size: 18px;
      margin-bottom: 10px;
    }

    .button-container {
      text-align: center;
      margin: 25px 0;
    }

    .cta-button {
      background-color: #9bc6a6;
      color: #ffffff !important;
      padding: 12px 20px;
      text-decoration: none;
      border-radius: 5px;
      display: inline-block;
      font-weight: bold;
    }

    .cta-button:hover {
      background-color: #84b495;
    }

    .footer {
      background-color: #f0f0f0;
      padding: 20px;
      text-align: center;
      font-size: 13px;
      color: #848e9c;
    }

    .signature {
      margin-top: 30px;
    }

    @media only screen and (max-width: 600px) {
      .content {
        padding: 15px;
      }
    }
  </style>
</head>
<body>

  <div class="container">
    <div class="email-card">

      <!-- HEADER -->
            <div class="header">
                <img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1774223918/5_mvgkea.png" alt="Logo"
                    style="height: 300px; display:block; margin:0 auto 10px; width: 300px;">
            </div>


      <!-- CONTENT -->
      <div class="content">

        <div>{{GREETING}},</div>
        <br/>

        <div>
          {{MAIN_MESSAGE}}
        </div>

        <!-- CTA BUTTON -->
        {{action_button}}

        <div>
          {{SECONDARY_MESSAGE}}
        </div>

        <!-- SIGNATURE -->
        <div class="signature">
          <div>Cordialement,</div>
          <div><strong>L'équipe {{APP_NAME}}</strong></div>
        </div>
      </div>

      <!-- FOOTER -->
      <div class="footer">
        <div>{{FOOTER_TEXT}}</div>
        <div>
          <a href="{{UNSUBSCRIBE_LINK}}" style="color:#848e9c; text-decoration: underline;">
            Se désinscrire
          </a>
        </div>
      </div>

    </div>
  </div>

</body>
</html>
"""

affliation_email_template = """<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nouvelle commission - PyCon Togo 2026</title>

    <style>
        body {
            margin: 0;
            padding: 0;
            background: #f4f6f9;
            font-family: Arial, Helvetica, sans-serif;
            color: #333;
        }

        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, .08);
        }

        .header {
            padding: 20px;
            text-align: center;
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
        }

        .header h1 {
            margin: 0;
            font-size: 28px;
        }

        .content {
            padding: 35px;
        }

        .content h2 {
            margin-top: 0;
            color: #16a34a;
        }

        .box {
            background: #f8fafc;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
        }

        .box table {
            width: 100%;
            border-collapse: collapse;
        }

        .box td {
            padding: 8px 0;
        }

        .label {
            color: #666;
        }

        .value {
            text-align: right;
            font-weight: bold;
        }

        .amount {
            color: #16a34a;
            font-size: 26px;
        }



        .note {
            margin-top: 30px;
            font-size: 14px;
            color: #666;
            line-height: 1.6;
        }

        .footer {
            text-align: center;
            padding: 25px;
            font-size: 13px;
            color: #777;
            background: #f8fafc;
        }

        @media(max-width:600px) {

            .content {
                padding: 25px;
            }

            .header h1 {
                font-size: 24px;
            }

            .amount {
                font-size: 22px;
            }

        }
    </style>

</head>

<body>

    <div class="container">
        <div class="header">
            <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/Slide%2016_9%20-%205%20(2).png" alt="Logo"
                style="height: 300px; display:block; width: 100%;">
        </div>


        <div class="content">


            <h2>Bonjour {{ affiliate_name }},</h2>

            <p>
                Bonne nouvelle !
                Une personne vient de s'inscrire au <strong>{{ event_name }}</strong> en utilisant votre lien de
                parrainage.
            </p>

            <div class="box">

                <table>

                    <tr>
                        <td class="label">Type de ticket</td>
                        <td class="value">{{ ticket_name }}</td>
                    </tr>

          

                    <tr>
                        <td class="label">Commission gagnée</td>
                        <td class="value amount">{{ commission_amount }}</td>
                    </tr>

                    <tr>
                        <td class="label">Date</td>
                        <td class="value">{{ purchase_date }}</td>
                    </tr>

                    <tr>
                        <td class="label">Référence</td>
                        <td class="value">{{ referral_id }}</td>
                    </tr>

                    <tr>
                        <td class="label">Statut</td>
                        <td class="value">En attente de versement</td>
                    </tr>

                </table>

            </div>

            <p>
                Cette vente a bien été enregistrée dans notre système et votre commission est désormais associée à votre
                compte.
            </p>

            <div class="note">

                <strong>Important :</strong>

                <ul>
                    <li>Cette notification confirme uniquement l'enregistrement de votre commission.</li>
                    <li>Le paiement sera effectué conformément aux règles du programme de parrainage.</li>
                    <li>Conservez cet email pour vos archives.</li>
                </ul>

            </div>

        </div>

        <div class="footer">

            <strong>Python Software Community of Togo</strong><br>
            Building the Future of Python in West Africa<br><br>

            Cet email a été envoyé automatiquement. Merci de ne pas y répondre.

        </div>

    </div>

</body>

</html>
"""

affliation_plain_text_template = """Bonjour {{ affiliate_name }},
Bonne nouvelle ! Une personne vient de s'inscrire au {{ event_name }} en utilisant votre lien de parrainage.

Détails de la transaction :
- Type de ticket : {{ ticket_name }}
- Commission gagnée : {{ commission_amount }}
- Date : {{ purchase_date }}
- Référence : {{ referral_id }}
Statut : En attente de versement

Cette vente a bien été enregistrée dans notre système et votre commission est désormais associée à votre compte.
Important :
- Cette notification confirme uniquement l'enregistrement de votre commission.
- Le paiement sera effectué conformément aux règles du programme de parrainage.
- Conservez cet email pour vos archives. 

Python Software Community of Togo
Building the Future of Python in West Africa
Cet email a été envoyé automatiquement. Merci de ne pas y répondre.
"""


def generate_affiliation_email_content(affiliate_name, ticket_name, commission_amount, purchase_date, referral_id, event_name, currency_symbol="F CFA"):
    email_html_content = affliation_email_template.replace(
        "{{ affiliate_name }}", affiliate_name)
    email_html_content = email_html_content.replace(
        "{{ ticket_name }}", ticket_name)
    # email_html_content = email_html_content.replace(
    #    "{{ ticket_price }}", ticket_price)
    email_html_content = email_html_content.replace(
        "{{ commission_amount }}", f"{commission_amount} {currency_symbol}")
    email_html_content = email_html_content.replace(
        "{{ purchase_date }}", purchase_date)
    email_html_content = email_html_content.replace(
        "{{ referral_id }}", referral_id)
    email_html_content = email_html_content.replace(
        "{{ event_name }}", event_name)

    email_plain_text_content = affliation_plain_text_template.replace(
        "{{ affiliate_name }}", affiliate_name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{ ticket_name }}", ticket_name)
    # email_plain_text_content = email_plain_text_content.replace(
    #    "{{ ticket_price }}", ticket_price)
    email_plain_text_content = email_plain_text_content.replace(
        "{{ commission_amount }}", f"{commission_amount} {currency_symbol}")
    email_plain_text_content = email_plain_text_content.replace(
        "{{ purchase_date }}", purchase_date)
    email_plain_text_content = email_plain_text_content.replace(
        "{{ referral_id }}", referral_id)
    email_plain_text_content = email_plain_text_content.replace(
        "{{ event_name }}", event_name)
    return email_html_content, email_plain_text_content


def generate_email(org_name="Python Community"):
    html_content = f"""
    <!DOCTYPE html >
    <html >

    <body style = "margin:0; padding:0; background:#f4f4f4; font-family:Arial, sans-serif;" >

        <table width = "100%" cellpadding = "0" cellspacing = "0" style = "padding:20px;" >
            <tr >
                <td align = "center" >

                    <table width = "600" cellpadding = "0" cellspacing = "0"
                        style = "background:#ffffff; border-radius:8px; padding:25px;" >

                        <!-- Logo - ->
                        <tr >
                            <td align = "center" >
                                <img src = "https://res.cloudinary.com/dvg7vky5o/image/upload/v1774223918/5_mvgkea.png"
                                    alt = "PyCon Togo 2026" width = "140"
                                    style = "display:block; max-width:100%; height:auto;" >
                            </td >
                        </tr >

                        <!-- Body - ->
                        <tr >
                            <td style = "font-size:14px; color:#555; line-height:1.6; padding-top:15px;" >

                                <p > Dear {org_name} Team, < /p >

                                <p >
                                    My name is <strong > Wachiou Bouraima (Wasiu Ibrahim) < /strong >, and I am a member of the
                                    organizing team of < strong > PyCon Togo 2026 < /strong > .
                                </p >

                                <p >
                                    Following a successful first edition, we are currently preparing our second edition, with
                                    the ambition of strengthening the Python ecosystem in Togo and across West Africa.
                                </p >

                                <p >
                                    In this context, I am reaching out to connect with Python communities around the world and
                                    learn from teams like yours.
                                </p >

                                <p >
                                    I came across < strong > {org_name} < /strong > and was impressed by your work in growing your
                                    local Python community.
                                </p >

                                <p >
                                    Your support could greatly help us as we continue building and scaling our conference.
                                </p >

                                <p > We would especially appreciate: < /p >

                                <ul style = "padding-left:18px;" >
                                    <li > Insights on organizing and scaling a PyCon event < /li >
                                    <li > Guidance on sponsorship strategies < /li >
                                    <li > Introductions to potential partners or sponsors < /li >
                                    <li > Sharing our initiative within your community < /li >
                                </ul >

                                <p >
                                    Learn more about our event: < br >
                                    <a href = "https://pycon.pytogo.org"
                                      style = "color:#3776AB; word-break:break-word;" >
                                        https: // pycon.pytogo.org
                                    </a >
                                </p >

                                <p >
                                    We would be happy to schedule a short call if you are available.
                                </p >

                                <p >
                                    Thank you for your time and for supporting the global Python community.
                                </p >

                                <p >
                                    Best regards, < br >
                                    <strong > Wachiou Bouraima(Wasiu Ibrahim) < /strong > <br >
                                    PyCon Togo Organizing Team
                                </p >

                            </td >
                        </tr >

                    </table >

                </td >
            </tr >
        </table >

    </body >

    </html >
    """
    return html_content


def generate_plain_text_email(org_name="Python Community"):
    return f"""
    Dear {org_name} Team,

    My name is Wachiou Bouraima(Wasiu Ibrahim), and I am a member of the organizing team of PyCon Togo 2026.

    Following a successful first edition, we are currently preparing our second edition, with the ambition of strengthening the Python ecosystem in Togo and across West Africa.

    In this context, I am reaching out to connect with Python communities around the world and learn from teams like yours.

    I came across {org_name} and was impressed by your work in growing your local Python community.

    Your support could greatly help us as we continue building and scaling our conference.

    We would especially appreciate:
    - Insights on organizing and scaling a PyCon event
    - Guidance on sponsorship strategies
    - Introductions to potential partners or sponsors
    - Sharing our initiative within your community

    Learn more about our event:
    https: // pycon.pytogo.org

    We would be happy to schedule a short call if you are available.

    Thank you for your time and for supporting the global Python community.

    Best regards,
    Wachiou Bouraima(Wasiu Ibrahim)
    PyCon Togo Organizing Team
    """


def generate_action_button(action_url, action_text):
    if action_url and action_text:
        return f"""
        <div class = "button-container" >
          <a href = "{action_url}" class = "cta-button" > {action_text} < /a >
        </div >
        """
    return ""


def generate_email_content(business_name, message_content, second_message_content, action_url=None, action_text=None, greeting="Cher Utilisateur"):
    action_button = generate_action_button(action_url, action_text)
    return hmlt_template.replace("{{APP_NAME}}", business_name) \
        .replace("{{GREETING}}", greeting) \
        .replace("{{MAIN_MESSAGE}}", message_content) \
        .replace("{{SECONDARY_MESSAGE}}", second_message_content) \
        .replace("{{action_button}}", action_button) \
        .replace("{{FOOTER_TEXT}}", f"Vous recevez cet email car vous êtes inscrit sur {business_name}.") \
        .replace("{{UNSUBSCRIBE_LINK}}", "https://www.pycontg.pytogo.org/unsubscribe")


if __name__ == "__main__":
    # Example usage
    hmlt_template = generate_email(
        org_name="Python Community",
        event="votre événement local",
        business_name="PyCon Togo"
    )

    print(hmlt_template)
