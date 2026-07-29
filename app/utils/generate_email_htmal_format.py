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

team_email_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f4f6f8;
            font-family: Arial, Helvetica, sans-serif;
            color: #333333;
        }

        .container {
            max-width: 600px;
            margin: 30px auto;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .header {
            background: #111827;
            color: white;
            padding: 25px;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 22px;
        }

        .content {
            padding: 30px;
        }

        .badge {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-bottom: 20px;
        }

        .warning-box {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            color: #9a3412;
            font-size: 14px;
            line-height: 1.5;
        }

        .info-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }

        .info-row {
            margin-bottom: 12px;
        }

        .label {
            font-weight: bold;
            color: #111827;
        }

        .message {
            background: #ffffff;
            border-left: 4px solid #2563eb;
            padding: 15px;
            margin-top: 15px;
            line-height: 1.6;
        }

        .footer {
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            line-height: 1.6;
        }

    </style>

</head>

<body>

<div class="container">

    <div class="header">
        <h1>{{app_name}}</h1>
    </div>


    <div class="content">

        <span class="badge">
            {{notification_type}}
        </span>


        <h2>{{title}}</h2>


        <p>
            Bonjour équipe {{team_name}},
        </p>


        <!-- Avertissement sécurité -->
        <div class="warning-box">

            <strong>⚠️ Attention :</strong><br><br>

            Ce message provient d'un formulaire public soumis depuis la plateforme.
            Les informations fournies par l'expéditeur n'ont pas été vérifiées.

            <br><br>

            Elles peuvent contenir des erreurs, des informations incomplètes
            ou du contenu indésirable.

            <br><br>

            Veuillez rester vigilant avant de répondre à ce message,
            d'ouvrir des liens ou d'effectuer toute action demandée par l'expéditeur.

        </div>



        <p>
            Un nouveau message vient d'être reçu depuis votre plateforme.
            Voici les informations :
        </p>



        <div class="info-box">


            <div class="info-row">
                <span class="label">Nom :</span>
                {{name}}
            </div>


            <div class="info-row">
                <span class="label">Email :</span>
                {{email}}
            </div>


            <div class="info-row">
                <span class="label">Phone :</span>
                {{phone}}
            </div>


            <div class="info-row">
                <span class="label">Sujet :</span>
                {{subject}}
            </div>


            <div class="info-row">
                <span class="label">Date :</span>
                {{date}}
            </div>


        </div>



        <h3>Message reçu</h3>


        <div class="message">
            {{message}}
        </div>



    </div>



    <div class="footer">

        Cet email a été envoyé automatiquement par
        <strong>{{app_name}}</strong>.

        <br><br>

        ⚠️ Rappel sécurité : les messages reçus via les formulaires publics
        peuvent provenir de sources non vérifiées.

        <br>

        Ne cliquez pas sur des liens suspects et vérifiez toujours
        les informations avant toute action.

        <br><br>

        Merci de traiter cette demande rapidement.

    </div>


</div>


</body>
</html>
"""

team_plain_text_template = """Bonjour équipe {{team_name}},

⚠️ Attention :
Ce message provient d'un formulaire public. Les informations fournies par l'expéditeur n'ont pas été vérifiées.
Elles peuvent être erronées ou contenir du contenu indésirable.
Veuillez vérifier les informations avant de répondre ou d'ouvrir des liens éventuels.

Un nouveau message vient d'être reçu depuis votre plateforme.
Voici les informations :
- Nom : {{name}}
- Email : {{email}}
- Phone : {{phone}}
- Sujet : {{subject}}
- Date : {{date}}

Message reçu :
{{message}}

Cet email a été envoyé automatiquement par {{app_name}}.

⚠️ Rappel sécurité :
Ne cliquez pas sur des liens suspects et vérifiez toujours les informations avant toute action.

Merci de traiter cette demande rapidement.
"""


ticket_team_email_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f4f6f8;
            font-family: Arial, Helvetica, sans-serif;
            color: #333333;
        }

        .container {
            max-width: 600px;
            margin: 30px auto;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .header {
            background: #111827;
            color: white;
            padding: 25px;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 22px;
        }

        .content {
            padding: 30px;
        }

        .badge {
            display: inline-block;
            background: #16a34a;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-bottom: 20px;
        }

        .info-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }

        .info-row {
            margin-bottom: 12px;
        }

        .label {
            font-weight: bold;
            color: #111827;
        }

        .payment-box {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }

        .warning-box {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            color: #9a3412;
            line-height: 1.5;
        }

        .button {
            display: inline-block;
            margin-top: 15px;
            padding: 12px 20px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }

        .footer {
            background: #f9fafb;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            line-height: 1.6;
        }

    </style>

</head>

<body>

<div class="container">


    <div class="header">
        <h1>{{app_name}}</h1>
    </div>



    <div class="content">


        <span class="badge">
            Nouvelle inscription ticket
        </span>


        <h2>Nouvelle inscription reçue</h2>


        <p>
            Bonjour équipe billetterie,
        </p>


        <p>
            Une nouvelle inscription vient d'être enregistrée sur la plateforme.
            Voici les informations du participant :
        </p>



        <div class="info-box">


            <div class="info-row">
                <span class="label">Nom complet :</span>
                {{name}}
            </div>


            <div class="info-row">
                <span class="label">Email :</span>
                {{email}}
            </div>


            <div class="info-row">
                <span class="label">Téléphone :</span>
                {{phone}}
            </div>


            <div class="info-row">
                <span class="label">Type de ticket :</span>
                {{ticket_type}}
            </div>


            <div class="info-row">
                <span class="label">Montant :</span>
                {{amount}}
            </div>
               <div class="info-row">
                <span class="label">Voucher code :</span>
                {{voucher_code}}
            </div>



            <div class="info-row">
                <span class="label">Statut paiement :</span>
                {{payment_status}}
            </div>


            <div class="info-row">
                <span class="label">Date d'inscription :</span>
                {{date}}
            </div>


        </div>




        <div class="payment-box">

            <strong>Lien de paiement :</strong>

            <br><br>

            {{payment_url}}

            <br>

        </div>





        <div class="warning-box">

            <strong>⚠️ Suivi nécessaire :</strong>

            <br><br>

            Si le paiement n'est pas confirmé après 48 heures,
            merci de contacter le participant afin de vérifier
            sa situation et l'accompagner dans la finalisation
            de son inscription.

        </div>




    </div>




    <div class="footer">

        Cet email a été envoyé automatiquement par
        <strong>{{app_name}}</strong>.

        <br><br>

        Notification interne - Équipe billetterie.

    </div>


</div>


</body>
</html>
"""

ticket_team_plain_text_template = """Bonjour équipe billetterie,

Une nouvelle inscription vient d'être enregistrée sur la plateforme.

Voici les informations du participant :

- Nom complet : {{name}}
- Email : {{email}}
- Téléphone : {{phone}}
- Type de ticket : {{ticket_type}}
- Montant : {{amount}}
- voucher code : {{voucher_code}}
- Statut paiement : {{payment_status}}
- Date d'inscription : {{date}}

Lien de paiement :
{{payment_url}}

⚠️ Suivi nécessaire :

Si le paiement n'est pas confirmé après 48 heures,
merci de contacter le participant afin de vérifier sa situation
et l'accompagner dans la finalisation de son inscription.

Cet email a été envoyé automatiquement par {{app_name}}.

Notification interne - Équipe billetterie.
"""


def generate_ticket_team_email_content(app_name, name, email, ticket_type, amount, payment_status, date, payment_url, voucher_code="N/A", phone="N/A"):
    amount = f"{str(amount)} F CFA" if amount else "N/A"
    email_html_content = ticket_team_email_template.replace(
        "{{app_name}}", app_name)
    email_html_content = email_html_content.replace("{{name}}", name)
    email_html_content = email_html_content.replace("{{email}}", email)
    email_html_content = email_html_content.replace(
        "{{phone}}", phone if phone else "N/A")
    email_html_content = email_html_content.replace(
        "{{ticket_type}}", ticket_type)
    email_html_content = email_html_content.replace("{{amount}}", amount)
    email_html_content = email_html_content.replace(
        "{{payment_status}}", payment_status)
    email_html_content = email_html_content.replace("{{date}}", date.strftime(
        "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date))
    email_html_content = email_html_content.replace(
        "{{payment_url}}", payment_url)
    email_html_content = email_html_content.replace(
        "{{voucher_code}}", voucher_code if voucher_code else "N/A")

    email_plain_text_content = ticket_team_plain_text_template.replace(
        "{{app_name}}", app_name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{name}}", name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{email}}", email)
    email_plain_text_content = email_plain_text_content.replace(
        "{{phone}}", phone if phone else "N/A")
    email_plain_text_content = email_plain_text_content.replace(
        "{{ticket_type}}", ticket_type)
    email_plain_text_content = email_plain_text_content.replace(
        "{{amount}}", amount)
    email_plain_text_content = email_plain_text_content.replace(
        "{{payment_status}}", payment_status)
    email_plain_text_content = email_plain_text_content.replace("{{date}}", date.strftime(
        "%Y-%m-%d %H:%M:%S") if hasattr(date, 'strftime') else str(date))
    email_plain_text_content = email_plain_text_content.replace(
        "{{payment_url}}", payment_url)
    email_plain_text_content = email_plain_text_content.replace(
        "{{voucher_code}}", voucher_code if voucher_code else "N/A")

    return email_html_content, email_plain_text_content


def generate_team_email_content(app_name, team_name, notification_type, title, name, email, subject, date, message, phone=None):
    email_html_content = team_email_template.replace("{{app_name}}", app_name)
    email_html_content = email_html_content.replace("{{team_name}}", team_name)
    email_html_content = email_html_content.replace(
        "{{notification_type}}", notification_type)
    email_html_content = email_html_content.replace("{{title}}", title)
    email_html_content = email_html_content.replace("{{name}}", name)
    email_html_content = email_html_content.replace("{{email}}", email)
    email_html_content = email_html_content.replace(
        "{{phone}}", phone if phone else "N/A")
    email_html_content = email_html_content.replace("{{subject}}", subject)
    email_html_content = email_html_content.replace("{{date}}", date)
    email_html_content = email_html_content.replace("{{message}}", message)

    email_plain_text_content = team_plain_text_template.replace(
        "{{app_name}}", app_name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{team_name}}", team_name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{notification_type}}", notification_type)
    email_plain_text_content = email_plain_text_content.replace(
        "{{title}}", title)
    email_plain_text_content = email_plain_text_content.replace(
        "{{name}}", name)
    email_plain_text_content = email_plain_text_content.replace(
        "{{email}}", email)
    email_plain_text_content = email_plain_text_content.replace(
        "{{phone}}", phone if phone else "N/A")
    email_plain_text_content = email_plain_text_content.replace(
        "{{subject}}", subject)
    email_plain_text_content = email_plain_text_content.replace(
        "{{date}}", date)
    email_plain_text_content = email_plain_text_content.replace(
        "{{message}}", message)

    return email_html_content, email_plain_text_content


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
    <!DOCTYPE html>
    <html>

    <body style = "margin:0; padding:0; background:#f4f4f4; font-family:Arial, sans-serif;">

        <table width = "100%" cellpadding = "0" cellspacing = "0" style = "padding:20px;">
            <tr>
                <td align = "center">

                    <table width = "600" cellpadding = "0" cellspacing = "0"
                        style = "background:#ffffff; border-radius:8px; padding:25px;">

                        <!-- Logo - ->
                        <tr>
                            <td align = "center">
                                <img src = "https://res.cloudinary.com/dvg7vky5o/image/upload/v1774223918/5_mvgkea.png"
                                    alt = "PyCon Togo 2026" width = "140"
                                    style = "display:block; max-width:100%; height:auto;">
                            </td>
                        </tr>

                        <!-- Body - ->
                        <tr>
                            <td style = "font-size:14px; color:#555; line-height:1.6; padding-top:15px;">

                                <p> Dear {org_name} Team, </p>

                                <p>
                                    My name is <strong> Wachiou Bouraima (Wasiu Ibrahim) </strong>, and I am a member of the
                                    organizing team of <strong> PyCon Togo 2026 </strong> .
                                </p>

                                <p>
                                    Following a successful first edition, we are currently preparing our second edition, with
                                    the ambition of strengthening the Python ecosystem in Togo and across West Africa.
                                </p>

                                <p>
                                    In this context, I am reaching out to connect with Python communities around the world and
                                    learn from teams like yours.
                                </p>

                                <p>
                                    I came across <strong> {org_name} </strong> and was impressed by your work in growing your
                                    local Python community.
                                </p>

                                <p>
                                    Your support could greatly help us as we continue building and scaling our conference.
                                </p>

                                <p> We would especially appreciate: </p>

                                <ul style = "padding-left:18px;">
                                    <li> Insights on organizing and scaling a PyCon event </li>
                                    <li> Guidance on sponsorship strategies </li>
                                    <li> Introductions to potential partners or sponsors </li>
                                    <li> Sharing our initiative within your community </li>
                                </ul>

                                <p>
                                    Learn more about our event: <br />
                                    <a href = "https://pycon.pytogo.org"
                                      style = "color:#3776AB; word-break:break-word;">
                                        https: // pycon.pytogo.org
                                    </a>
                                </p>

                                <p>
                                    We would be happy to schedule a short call if you are available.
                                </p>

                                <p>
                                    Thank you for your time and for supporting the global Python community.
                                </p>

                                <p>
                                    Best regards, <br />
                                    <strong> Wachiou Bouraima(Wasiu Ibrahim) </strong> <br>
                                    PyCon Togo Organizing Team
                                </p>

                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>

    </html>
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
        <div class = "button-container">
          <a href = "{action_url}" class = "cta-button"> {action_text} </a>
        </div>
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

    html_content, plain_text_content = generate_ticket_team_email_content(
        app_name="PyCon Togo 2026",
        name="John Doe",
        email="john.doe@example.com",
        phone="+228 90 00 00 00",
        ticket_type="Standard",
        amount="50,000 F CFA",
        payment_status="En attente",
        date="2024-06-15 14:30:00",
        payment_url="https://www.pycontg.pytogo.org/payment/12345"
    )

    print(html_content)
