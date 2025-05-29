
# VANET Secure Simulation Project

This project implements a secure communication system for Vehicular Ad Hoc Networks (VANETs) using Python. It focuses on message integrity and authentication through cryptographic techniques.

---

## 🔐 Key Features

- **Vehicle Simulation**: Simulates vehicle movement and collision detection.
- **Message Hashing**: Uses SHA-256, MD5, SHA-1, BLAKE2b, and SHA3-256 for ensuring message integrity.
- **Digital Signatures**: Employs RSA for signing and verifying messages to ensure authenticity.
- **Security Validation**: Detects tampered messages and verifies the sender's identity.
- **Performance Visualization**:
  - Vehicle Speeds Over Time
  - Vehicle Positions Over Time
  - Hash Generation Time (Boxplot)

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install matplotlib pandas cryptography
```

---

## 🚀 How to Run

```bash
python vanet_secure_simulation.py
```

The script simulates secure VANET communication and visualizes the results.

---

## 🧪 Output

- Terminal output indicating hash and signature verification status.
- Matplotlib plots showing:
  - Vehicle speed variation
  - Movement paths
  - Hash function performance

---

## 🧰 Tools & Libraries

- `cryptography` — for RSA key generation and signature verification
- `hashlib` — for cryptographic hash functions
- `matplotlib` & `pandas` — for data visualization and analysis

---

## 📌 Outcome

This simulation demonstrates a secure routing strategy for VANETs, using combined hash and digital signature verification to protect against message tampering and impersonation.
