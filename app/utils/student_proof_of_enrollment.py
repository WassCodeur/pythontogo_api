template = """<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>PyCon Togo 2026 – Student Submission Received</title>
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

        .header-image img {
            width: 100%;
            max-width: 600px;
            height: auto;
            display: block;
        }

        /* ===== STATUS BADGE ===== */
        .status-banner {
            background: linear-gradient(135deg, #fff8f0 0%, #fff3e8 100%);
            border-left: 4px solid #EF553C;
            margin: 0 36px 28px 36px;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
        }

        .status-badge {
            display: inline-block;
            background-color: #FFF0ED;
            color: #EF553C;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid #EF553C;
            margin-bottom: 8px;
        }

        .status-message {
            font-size: 13px;
            color: #555555;
            line-height: 1.6;
        }

        /* ===== BODY CONTENT ===== */
        .body-content {
            padding: 32px 36px 24px 36px;
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
            margin-bottom: 12px;
        }

        .intro-text {
            font-size: 15px;
            color: #444444;
            line-height: 1.7;
            margin-bottom: 8px;
        }

        .intro-text .highlight {
            color: #EF553C;
            font-weight: 700;
        }

        /* ===== INFO CARD ===== */
        .info-card {
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            overflow: hidden;
            margin: 0 36px 28px 36px;
        }

        .info-card-header {
            background-color: #f9f9f9;
            padding: 14px 20px;
            border-bottom: 1px solid #eeeeee;
        }

        .info-card-header p {
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #888888;
        }

        .info-details {
            width: 100%;
            border-collapse: collapse;
        }

        .info-details td {
            padding: 13px 20px;
            font-size: 14px;
            border-bottom: 1px solid #eeeeee;
        }

        .info-details tr:last-child td {
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

        .detail-value.status-pending {
            color: #D97706;
        }

        .detail-value.status-paid {
            color: #2DA44E;
        }

        /* ===== DOCUMENT LINK BUTTON ===== */
        .doc-section {
            padding: 0 36px 24px 36px;
        }

        .doc-title {
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #888888;
            margin-bottom: 12px;
        }

        .doc-link-box {
            border: 1px dashed #cccccc;
            border-radius: 8px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            background-color: #fafafa;
        }

        .doc-link-box .doc-icon {
            font-size: 22px;
        }

        .doc-link-box .doc-info {
            flex: 1;
        }

        .doc-link-box .doc-name {
            font-size: 14px;
            font-weight: 700;
            color: #111111;
            margin-bottom: 2px;
        }

        .doc-link-box .doc-meta {
            font-size: 12px;
            color: #888888;
        }

        .doc-view-btn {
            display: inline-block;
            background-color: #111111;
            color: #ffffff !important;
            font-size: 12px;
            font-weight: 700;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 6px;
            white-space: nowrap;
        }

        /* ===== TABLE FALLBACK for doc-link-box ===== */
        .doc-link-table {
            width: 100%;
            border-collapse: collapse;
            border: 1px dashed #cccccc;
            border-radius: 8px;
            background-color: #fafafa;
        }

        .doc-link-table td {
            padding: 14px;
            vertical-align: middle;
        }

        /* ===== TIMELINE / NEXT STEPS ===== */
        .steps-section {
            padding: 0 36px 24px 36px;
        }

        .section-title {
            font-size: 13px;
            font-weight: 800;
            color: #111111;
            margin-bottom: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .step-item {
            display: flex;
            gap: 14px;
            margin-bottom: 14px;
            align-items: flex-start;
        }

        .step-dot {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            font-size: 12px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }

        .step-dot.done {
            background-color: #2DA44E;
            color: #ffffff;
        }

        .step-dot.active {
            background-color: #EF553C;
            color: #ffffff;
        }

        .step-dot.pending {
            background-color: #eeeeee;
            color: #888888;
        }

        .step-content .step-label {
            font-size: 14px;
            font-weight: 700;
            color: #111111;
            margin-bottom: 2px;
        }

        .step-content .step-desc {
            font-size: 13px;
            color: #666666;
            line-height: 1.5;
        }

        /* Steps as table for email clients */
        .steps-table {
            width: 100%;
            border-collapse: collapse;
        }

        .steps-table td {
            padding: 6px 0;
            vertical-align: top;
        }

        .steps-table .dot-cell {
            width: 36px;
        }

        .divider {
            border: none;
            border-top: 1px solid #eeeeee;
            margin: 0 36px 24px 36px;
        }

        /* ===== NOTE ===== */
        .note-section {
            padding: 0 36px 24px 36px;
        }

        .note-box {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 16px 20px;
            font-size: 13px;
            color: #555555;
            line-height: 1.7;
        }

        .note-box strong {
            color: #111111;
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

        /* ===== FOOTER DECORATIVE ===== */
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

        @media only screen and (max-width: 620px) {
            .email-wrapper {
                padding: 0 !important;
            }

            .email-container {
                border-radius: 0 !important;
            }

            .body-content {
                padding: 24px 20px 16px 20px !important;
            }

            .status-banner {
                margin: 0 20px 20px 20px !important;
            }

            .info-card {
                margin: 0 20px 20px 20px !important;
            }

            .doc-section {
                padding: 0 20px 20px 20px !important;
            }

            .steps-section {
                padding: 0 20px 20px 20px !important;
            }

            .note-section {
                padding: 0 20px 20px 20px !important;
            }

            .divider {
                margin: 0 20px 20px 20px !important;
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

                        <!-- HEADER -->
                        <div class="header-image">
                            <img src="https://ik.imagekit.io/foscyymdh/pythontogo/student_ids/under_review_header.png"
                                alt="PyCon Togo 2026" width="600" />
                        </div>

                        <!-- BODY -->
                        <div class="body-content">
                            <h1 class="title">Payment Confirmed –<br>Proof of Student Status Under Review</h1>
                            <p class="greeting">Hello {{firstName}},</p>
                            <p class="intro-text">
                                Great news, your payment has been <span class="highlight">successfully
                                    confirmed</span>.
                                Thank you for registering for PyCon Togo 2026.
                            </p>
                            <p class="intro-text" style="margin-top: 10px;">
                                We have received your proof of student status and our team is currently reviewing it.
                                We will get back to you <span class="highlight">within 24 hours</span> with further
                                details about your ticket.
                            </p>
                        </div>

                        <!-- STATUS BANNER -->
                        <div class="status-banner">
                            <div class="status-badge"> Under Review</div>
                            <p class="status-message">
                                Your document has been submitted and is being verified by our team. No further action is
                                needed on your end at this time.
                            </p>
                        </div>

                        <!-- REGISTRATION SUMMARY CARD -->
                        <div class="info-card" style="margin: 0 36px 28px 36px;">
                            <div class="info-card-header">
                                <p>Registration Summary</p>
                            </div>
                            <table class="info-details" role="presentation">
                                <tr>
                                    <td class="detail-label">Attendee:</td>
                                    <td class="detail-value">{{FULL_NAME}}</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">Ticket Type:</td>
                                    <td class="detail-value">Student Pass</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">Registration ID:</td>
                                    <td class="detail-value">{{REGISTRATION_ID}}</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">Payment Status:</td>
                                    <td class="detail-value status-paid">✓ Confirmed</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">Document Review:</td>
                                    <td class="detail-value status-pending"> Pending</td>
                                </tr>
                                <tr>
                                    <td class="detail-label">Submitted On:</td>
                                    <td class="detail-value">{{SUBMISSION_DATE}}</td>
                                </tr>
                            </table>
                        </div>

                        <!-- SUBMITTED DOCUMENT LINK -->
                        <div class="doc-section">
                            <p class="doc-title"> Your Submitted Document</p>
                            <table class="doc-link-table" role="presentation" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td class="dot-cell" style="padding-left: 16px; font-size: 22px; width: 40px;">📎
                                    </td>
                                    <td style="padding: 14px 8px;">
                                        <p
                                            style="font-size: 14px; font-weight: 700; color: #111111; margin-bottom: 2px;">
                                            {{DOCUMENT_NAME}}</p>
                                        <p style="font-size: 12px; color: #888888;">Submitted for student verification
                                        </p>
                                    </td>
                                    <td style="padding: 14px 16px 14px 8px; white-space: nowrap;">
                                        <a href="{{DOCUMENT_URL}}" class="doc-view-btn" target="_blank">View
                                            Document</a>
                                    </td>
                                </tr>
                            </table>
                        </div>

                        <hr class="divider" />

                        <!-- NEXT STEPS -->
                        <div class="steps-section">
                            <p class="section-title">What happens next?</p>
                            <table class="steps-table" role="presentation" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td class="dot-cell">
                                        <div
                                            style="width: 28px; height: 28px; border-radius: 50%; background-color: #2DA44E; text-align: center; line-height: 28px; font-size: 12px; font-weight: 800; color: #ffffff;">
                                            ✓</div>
                                    </td>
                                    <td style="padding-bottom: 14px;">
                                        <p
                                            style="font-size: 14px; font-weight: 700; color: #111111; margin-bottom: 2px;">
                                            Payment Confirmed</p>
                                        <p style="font-size: 13px; color: #666666; line-height: 1.5;">Your payment has
                                            been processed successfully.</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="dot-cell">
                                        <div
                                            style="width: 28px; height: 28px; border-radius: 50%; background-color: #EF553C; text-align: center; line-height: 28px; font-size: 12px; font-weight: 800; color: #ffffff;">
                                            2</div>
                                    </td>
                                    <td style="padding-bottom: 14px;">
                                        <p
                                            style="font-size: 14px; font-weight: 700; color: #111111; margin-bottom: 2px;">
                                            Document Under Review</p>
                                        <p style="font-size: 13px; color: #666666; line-height: 1.5;">Our team is
                                            currently reviewing your proof of student status. This usually takes less
                                            than 24 hours.</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="dot-cell">
                                        <div
                                            style="width: 28px; height: 28px; border-radius: 50%; background-color: #eeeeee; text-align: center; line-height: 28px; font-size: 12px; font-weight: 800; color: #888888;">
                                            3</div>
                                    </td>
                                    <td style="padding-bottom: 0;">
                                        <p
                                            style="font-size: 14px; font-weight: 700; color: #888888; margin-bottom: 2px;">
                                            Ticket Issued</p>
                                        <p style="font-size: 13px; color: #999999; line-height: 1.5;">Once approved,
                                            you'll receive a confirmation email with your student ticket details.</p>
                                    </td>
                                </tr>
                            </table>
                        </div>

                        <hr class="divider" />

                        <!-- NOTE -->
                        <div class="note-section">
                            <div class="note-box">
                                <strong> Please note:</strong> If your document cannot be verified, our team will
                                contact you directly to request an alternative proof.
                                Make sure to check your inbox (and spam folder) over the next 24 hours.
                            </div>
                        </div>

                        <!-- SIGN OFF -->
                        <div class="signoff">
                            <p>We're excited to have you join the community <span class="rocket"></span></p>
                            <p class="signoff-name">PyCon Togo Team</p>
                        </div>

                        <!-- FOOTER DECORATIVE -->
                        <div class="footer-logos">
                            <img src="https://ik.imagekit.io/foscyymdh/pythontogo/pycontg26/snake.png"
                                alt="PyCon Togo Community" width="528" />
                        </div>

                        <!-- LEGAL FOOTER -->
                        <div class="legal-footer">
                            <p class="legal-text">
                                This email was sent to confirm receipt of your student registration for PyCon Togo
                                2026.<br />
                                Please do not reply to this email. For any queries, contact us through our official
                                channels.<br />
                                By attending the event, participants consent to photography and media coverage for
                                community and promotional purposes.
                            </p>

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

                            <div class="footer-brand">
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


def render_student_proof_under_review_email(first_name, full_name, registration_id, submission_date, document_name, document_url):
    email_content = template.replace("{{firstName}}", first_name)
    email_content = email_content.replace("{{FULL_NAME}}", full_name)
    email_content = email_content.replace(
        "{{REGISTRATION_ID}}", registration_id)
    email_content = email_content.replace(
        "{{SUBMISSION_DATE}}", submission_date)
    email_content = email_content.replace("{{DOCUMENT_NAME}}", document_name)
    email_content = email_content.replace("{{DOCUMENT_URL}}", document_url)
    return email_content
