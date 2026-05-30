template = """<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>PyCon Togo 2026 – Premium Pass Confirmed</title>
    <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
    <style>
        /* ===== RESET ===== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body,
        table,
        td,
        a {
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }

        table,
        td {
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }

        img {
            -ms-interpolation-mode: bicubic;
            border: 0;
            outline: none;
            text-decoration: none;
            display: block;
        }

        body {
            margin: 0 !important;
            padding: 0 !important;
            background-color: #f0f0f0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        /* ===== WRAPPER ===== */
        .email-wrapper {
            width: 100%;
            background-color: #f0f0f0;
            padding: 24px 0;
        }

        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.10);
        }

        /* ===== HEADER ===== */
        .header-image img {
            width: 100%;
            max-width: 600px;
            height: auto;
            display: block;
        }

        /* ===== BODY CONTENT ===== */
        .body-content {
            padding: 32px 36px 0 36px;
        }

        .title {
            font-size: 24px;
            font-weight: 800;
            color: #111111;
            line-height: 1.3;
            margin-bottom: 20px;
        }

        .greeting {
            font-size: 15px;
            color: #444444;
            margin-bottom: 8px;
        }

        .pass-confirmed {
            font-size: 15px;
            color: #444444;
            margin-bottom: 28px;
        }

        .pass-confirmed a,
        .pass-confirmed span.highlight {
            color: #EF553C;
            font-weight: 700;
            text-decoration: none;
        }

        /* ===== TICKET CARD ===== */
        .ticket-card {
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 28px;
            border: 1px solid #e5e5e5;
        }

        .ticket-image-wrapper {
            display: block;
            width: 100%;
        }

        .ticket-image-wrapper img {
            width: 100%;
            max-width: 600px;
            height: auto;
            display: block;
        }

        /* ===== TICKET DETAILS TABLE ===== */
        .ticket-details {
            width: 100%;
            border-collapse: collapse;
        }

        .ticket-details td {
            padding: 14px 20px;
            font-size: 14px;
            border-bottom: 1px solid #eeeeee;
        }

        .ticket-details tr:last-child td {
            border-bottom: none;
        }

        .detail-label {
            color: #666666;
            font-weight: 500;
            width: 40%;
        }

        .detail-value {
            color: #111111;
            font-weight: 700;
            text-align: right;
        }

        .detail-value.premium-pass {
            color: #EF553C;
            font-size: 15px;
        }

        /* ===== QR CODE SECTION ===== */
        .qr-section {
            padding: 20px;
            border-top: 1px solid #eeeeee;
            display: flex;
            align-items: flex-start;
            gap: 18px;
        }

        /* Fallback for email clients that don't support flex */
        .qr-table {
            width: 100%;
            border-collapse: collapse;
        }

        .qr-table td {
            vertical-align: middle;
            padding: 0;
        }

        .qr-code-cell {
            width: 110px;
            padding-right: 18px;
        }

        .qr-code-cell img {
            width: 100px;
            height: 100px;
            border-radius: 8px;
            border: 2px solid #eeeeee;
        }

        .qr-text {
            font-size: 13px;
            color: #555555;
            line-height: 1.6;
        }

        /* ===== DOWNLOAD BUTTON ===== */
        .btn-wrapper {
            text-align: center;
            padding: 24px 36px;
        }

        .btn-download {
            display: inline-block;
            background-color: #2DA44E;
            color: #ffffff !important;
            font-size: 15px;
            font-weight: 700;
            text-decoration: none;
            padding: 14px 36px;
            border-radius: 8px;
            letter-spacing: 0.3px;
        }

        /* ===== BENEFITS & NOTES ===== */
        .section {
            padding: 0 36px 24px 36px;
        }

        .section-title {
            font-size: 15px;
            font-weight: 800;
            color: #111111;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .section ul {
            padding-left: 18px;
        }

        .section ul li {
            font-size: 14px;
            color: #444444;
            margin-bottom: 6px;
            line-height: 1.6;
        }

        .divider {
            border: none;
            border-top: 1px solid #eeeeee;
            margin: 0 36px 24px 36px;
        }

        /* ===== QR ATTACHMENT NOTE ===== */
        .qr-note {
            padding: 0 36px 20px 36px;
            font-size: 14px;
            color: #444444;
        }

        .qr-note span {
            margin-right: 5px;
        }

        /* ===== SIGN OFF ===== */
        .signoff {
            padding: 0 36px 28px 36px;
            font-size: 15px;
            color: #444444;
        }

        .signoff .rocket {
            font-size: 18px;
        }

        .signoff-name {
            font-size: 15px;
            font-weight: 800;
            color: #111111;
            margin-top: 12px;
        }

        /* ===== FOOTER DECORATIVE LOGOS ===== */
        .footer-logos {
            text-align: center;
            padding: 10px 36px 0 36px;
        }

        .footer-logos img {
            max-width: 100%;
            height: auto;
            display: inline-block;
        }

        /* ===== LEGAL FOOTER ===== */
        .legal-footer {
            background-color: #f9f9f9;
            border-top: 1px solid #eeeeee;
            padding: 20px 36px;
        }

        .legal-text {
            font-size: 11px;
            color: #888888;
            line-height: 1.7;
            margin-bottom: 14px;
        }

        .social-icons {
            margin-bottom: 16px;
        }

        .social-icons a {
            display: inline-block;
            margin-right: 12px;
        }

        .social-icons a img {
            width: 22px;
            height: 22px;
        }

        .footer-brand {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }

        .footer-brand-logo img {
            height: 150px;
            width: auto;
        }

        .footer-copy {
            font-size: 11px;
            color: #888888;
        }

        /* ===== RESPONSIVE ===== */
        @media only screen and (max-width: 620px) {
            .email-wrapper {
                padding: 0 !important;
            }

            .email-container {
                border-radius: 0 !important;
            }

            .body-content {
                padding: 24px 20px 0 20px !important;
            }

            .section {
                padding: 0 20px 20px 20px !important;
            }

            .divider {
                margin: 0 20px 20px 20px !important;
            }

            .btn-wrapper {
                padding: 20px !important;
            }

            .qr-note {
                padding: 0 20px 16px 20px !important;
            }

            .signoff {
                padding: 0 20px 24px 20px !important;
            }

            .footer-logos {
                padding: 10px 20px 0 20px !important;
            }

            .legal-footer {
                padding: 16px 20px !important;
            }

            .title {
                font-size: 20px !important;
            }

            .footer-brand {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>

<body>
    <div class="email-wrapper">
        <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
            <tr>
                <td>
                    <div class="email-container">


                        <div class="header-image">
                            <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/Header.png"
                                alt="PyCon Togo 2026 – Event Ticket" width="600" />
                        </div>

                        <!-- ===== BODY CONTENT ===== -->
                        <div class="body-content">
                            <h1 class="title">Your PyCon Togo 2026 Premium Pass<br>is Confirmed</h1>
                            <p class="greeting">Hello {{firstName}},</p>
                            <p class="pass-confirmed">
                                Your <span class="highlight">PREMIUM PASS</span> has been successfully issued.
                            </p>
                        </div>
                        <div style="padding: 0 36px 0 36px;">
                            <div class="ticket-card">
                                <div class="ticket-image-wrapper">
                                    <img src="{{TICKET_URL}}" alt=" PyCon Togo 2026 Premium Pass – {{firstName}}"
                                        width="528" />
                                </div>

                                <!-- Ticket details -->
                                <table class="ticket-details" role="presentation">
                                    <tr>
                                        <td class="detail-label">Ticket Type:</td>
                                        <td class="detail-value premium-pass">PREMIUM PASS</td>
                                    </tr>
                                    <tr>
                                        <td class="detail-label">Attendee:</td>
                                        <td class="detail-value">{{FULL_NAME}}</td>
                                    </tr>
                                    <tr>
                                        <td class="detail-label">Ticket ID:</td>
                                        <td class="detail-value">{{TICKET_ID}}</td>
                                    </tr>
                                </table>

                                <!-- QR Code row -->
                                <table class="qr-table" role="presentation" style="border-top: 1px solid #eeeeee;">
                                    <tr>
                                        <td class="qr-code-cell"
                                            style="padding: 20px 0 20px 20px; width: 130px; vertical-align: middle;">
                                            <!-- Remplace le src par le lien du QR code généré dynamiquement via ImageKit -->
                                            <img src="{{QR_URL}}" alt="QR Code – {{TICKET_ID}}" width="100" height="100"
                                                style="border-radius: 8px; border: 2px solid #eeeeee;" />
                                        </td>
                                        <td style="padding: 20px 20px 20px 0; vertical-align: middle;">
                                            <p class="qr-text">
                                                Present this QR code at the registration desk for fast verification and
                                                venue access.
                                                This code is unique to your ticket and can only be used once for entry
                                                validation.
                                            </p>
                                        </td>
                                    </tr>
                                </table>

                                <!-- Valid For & Venue -->
                                <table class="ticket-details" role="presentation">
                                    <tr>
                                        <td class="detail-label">Valid For:</td>
                                        <td class="detail-value" style="font-size: 13px;">DAY 1 – DAY 3 (28-30 AUGUST
                                            2026)</td>
                                    </tr>
                                    <tr>
                                        <td class="detail-label">Venue:</td>
                                        <td class="detail-value">LOMÉ, TOGO</td>
                                    </tr>
                                </table>

                            </div><!-- /.ticket-card -->
                        </div>

                        <!-- ===== DOWNLOAD BUTTON ===== -->
                        <div class="btn-wrapper">
                            <!-- Remplace le href par le lien de téléchargement du ticket PDF/image -->
                            <a href="{{TICKET_URL}}" class="btn-download" download>
                                ⬇ &nbsp;Download Ticket
                            </a>
                        </div>

                        <!-- ===== PREMIUM PASS BENEFITS ===== -->
                        <div class="section">
                            <p class="section-title">Premium Pass Benefits:</p>
                            <ul>
                                <li>Full 3-day access to all sessions</li>
                                <li>Priority entry at event check-in</li>
                                <li>Access to exclusive networking sessions</li>
                                <li>Access to all workshops and closing day activities</li>
                                <li>Speaking opportunity at the event</li>
                                <li>PyCon Togo Community Membership</li>
                                <li>Dinner with industry leaders</li>
                            </ul>
                        </div>

                        <hr class="divider" />

                        <!-- ===== NOTE ===== -->
                        <div class="section">
                            <p class="section-title">Note:</p>
                            <ul>
                                <li>This pass is non-transferable.</li>
                                <li>QR code is required for entry scanning.</li>
                            </ul>
                        </div>

                        <!-- ===== QR ATTACHMENT NOTE ===== -->
                        <div class="qr-note">
                            <span>📎</span> Your QR code is attached to this email.
                        </div>

                        <!-- ===== SIGN OFF ===== -->
                        <div class="signoff">
                            <p>We're excited to have you grow with the community <span class="rocket">🚀</span></p>
                            <p class="signoff-name">PyCon Togo Team</p>
                        </div>

                        <!-- ===== FOOTER DECORATIVE LOGOS ===== -->
                        <!-- Remplace le src par le lien de l'image des logos/décorations du bas -->
                        <div class="footer-logos">
                            <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/snake.png"
                                alt="PyCon Togo Community" width="528" />
                        </div>

                        <!-- ===== LEGAL FOOTER ===== -->
                        <div class="legal-footer">
                            <p class="legal-text">
                                This ticket is electronically generated and valid only for the registered
                                attendee.<br />
                                PyCon Togo reserves the right to deny entry to duplicated, altered, or unauthorised
                                tickets.<br />
                                By attending the event, participants consent to photography and media coverage for
                                community and promotional purposes.
                            </p>

                            <!-- Social Icons -->
                            <div class="social-icons">
                                <a href="https://www.facebook.com/pytogoorg" target="_blank" rel="noopener">
                                    <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" alt="Facebook"
                                        width="22" height="22" />
                                </a>
                                <a href="https://x.com/TgPycon" target="_blank" rel="noopener">
                                    <img src="https://cdn-icons-png.flaticon.com/512/5969/5969020.png" alt="X (Twitter)"
                                        width="22" height="22" />
                                </a>
                                <a href="https://www.instagram.com/pycontg/" target="_blank" rel="noopener">
                                    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" alt="Instagram"
                                        width="22" height="22" />
                                </a>
                                <a href="https://www.youtube.com/@PythonTogo" target="_blank" rel="noopener">
                                    <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/Vector.png"
                                        alt="YouTube" width="22" height="22" />
                                </a>
                            </div>

                            <!-- Footer brand -->
                            <div class="footer-brand">
                                <!-- Remplace le src par le lien de ton logo PyCon Togo -->
                                <div class="footer-brand-logo">
                                    <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/PyContg26_gris.png"
                                        alt="PyCon Togo 26" />
                                </div>
                                <p class="footer-copy">© 2026 The Python Software Community Togo. All rights reserved.
                                </p>
                            </div>
                        </div>

                    </div>
                </td>
            </tr>
        </table>
    </div>
</body>

</html>"""


def render_premium_pass_email(first_name, full_name, ticket_id, ticket_url, qr_url):
    rendered_email = template.replace("{{firstName}}", first_name)
    rendered_email = rendered_email.replace("{{FULL_NAME}}", full_name)
    rendered_email = rendered_email.replace("{{TICKET_ID}}", ticket_id)
    rendered_email = rendered_email.replace("{{TICKET_URL}}", ticket_url)
    rendered_email = rendered_email.replace("{{QR_URL}}", qr_url)

    return rendered_email
