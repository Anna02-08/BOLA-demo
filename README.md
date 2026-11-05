# BOLA Vulnerability Demo

A simple educational REST API demonstrating **Broken Object Level Authorization (BOLA)**

## Project Overview

This project contains two REST API implementations:

- **Vulnerable API** – allows authenticated users to access other users' private documents by modifying the object ID.
- **Secure API** – verifies object ownership before granting access.


## Setup 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The API runs locally at `http://127.0.0.1:5000`.

## Demonstrating BOLA

Access Alice's own document:

```bash
curl -H "Authorization: Bearer alice-token" http://127.0.0.1:5000/vulnerable/documents/1
```

Access Bob's document using Alice's token:

```bash
curl -H "Authorization: Bearer alice-token" http://127.0.0.1:5000/vulnerable/documents/2
```

The vulnerable API exposes Bob's document.

Try the secure endpoint:

```bash
curl -i -H "Authorization: Bearer alice-token" http://127.0.0.1:5000/secure/documents/2
```

The secure API rejects unauthorized access.

