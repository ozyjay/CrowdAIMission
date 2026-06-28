# Data and Privacy

## Default position

Do not collect or store personal visitor data.

## Do not collect

- names;
- phone numbers;
- email addresses;
- login credentials;
- photos or video;
- audio recordings;
- precise device identifiers;
- open-ended personal stories.

## Visitor phone sessions

Use anonymous, temporary session IDs only if needed for rate limiting. Clear them regularly.

Do not persist session IDs after reset or shutdown unless explicitly approved and documented.

## Logs

Keep logs technical:

- route started;
- vote count;
- mission selected;
- model timeout;
- fallback triggered;
- validation failure category.

Avoid storing raw visitor text. Public MVP should not use visitor free text.

## QR signage

Suggested sign:

> Scan the QR code to help control the shared demo. No login is required. Please do not enter personal information.

## Staff response to privacy questions

Use:

> This demo is designed to use anonymous button taps only. It does not need your name, email, phone number, login, audio, or video. Staff can reset and clear the session.

## Shutdown data clearing

At shutdown:

- stop local services;
- clear temporary vote/session state;
- remove temporary logs if they include visitor input;
- confirm no audio/video recordings were saved;
- collect QR signage.
