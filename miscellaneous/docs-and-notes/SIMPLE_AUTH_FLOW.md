# Simple Byte-Bot Auth Flow

This is the exact simple login/register system you asked for.

## Register

Frontend sends:

```json
{
  "email": "harsh@example.com",
  "password": "password123",
  "name": "Harsh"
}
```

Backend route:

```text
POST /auth/register
```

Backend does this:

1. Checks MongoDB is connected.
2. Cleans the email by lowercasing it.
3. Checks whether that email already exists.
4. Hashes the password with bcrypt.
5. Stores this in MongoDB `users` collection:

```json
{
  "email": "harsh@example.com",
  "name": "Harsh",
  "password_hash": "bcrypt-hash-here",
  "auth_provider": "password",
  "is_email_verified": false
}
```

Important: the real password is not stored. Only `password_hash` is stored.

## Login

Frontend sends:

```json
{
  "email": "harsh@example.com",
  "password": "password123"
}
```

Backend route:

```text
POST /auth/login
```

Backend does this:

1. Finds the user in MongoDB by email.
2. If no user exists, login fails.
3. If user exists, compares typed password with stored `password_hash`.
4. If password is wrong, login fails.
5. If password is correct, backend returns:

```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "session_id": "bytebot-userid-here"
}
```

## Chat After Login

Frontend stores the token in `localStorage`.

When sending chat messages, frontend adds:

```text
Authorization: Bearer jwt-token-here
```

Backend reads that token and knows which user is chatting.

Then chat memory is stored in MongoDB `chat_messages`.

## What You Need For This To Work

Add this to `.env`:

```text
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=make-this-long-and-random
```

Restart FastAPI after editing `.env`.

## Your MongoDB Atlas String

You shared this Atlas template:

```text
mongodb+srv://dev07319_db_user:<db_password>@byte-bot.sr8eipf.mongodb.net/
```

Use it like this in `.env` after replacing `<db_password>`:

```text
MONGODB_URI=mongodb+srv://dev07319_db_user:YOUR_REAL_PASSWORD@byte-bot.sr8eipf.mongodb.net/bytebot?retryWrites=true&w=majority
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=make-this-long-and-random
```

Do not leave `<db_password>` in the active line. MongoDB will reject it.

If your password contains special characters like `@`, `/`, `#`, `%`, or `:`, URL encode it first.

## Current Login Choice

This project now uses only the simple email/password flow:

1. Register with email, name, and password.
2. Backend stores the user in MongoDB.
3. Login checks the typed email and password against MongoDB.
4. Backend returns a JWT token when the login is correct.

Social login is not part of the current version.
