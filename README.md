# Secure Blockchain Transactions

**Cryptographic Transaction Security & Validation Prototype**

A Python research prototype demonstrating how conventional authenticated encryption, password-based key derivation, transaction validation, and secure payload forwarding can be incorporated into a blockchain-oriented transaction pipeline.

> This project uses conventional cryptography. It is **not** a quantum-computing implementation and does **not** implement standardized post-quantum cryptographic algorithms.

---

## Overview

Blockchain applications frequently require security mechanisms outside the consensus layer itself.

Transaction information may need to be:

- authenticated
- validated
- encrypted
- protected against tampering
- transferred between processing layers

This repository demonstrates a simplified secure transaction pipeline using modern Python cryptographic primitives.

---

## Architecture

```text
                User
                 │
                 ▼
        Credential Validation
                 │
                 ▼
       Transaction Validation
                 │
                 ▼
          Key Derivation
             Scrypt
                 │
                 ▼
      Authenticated Encryption
             AES-GCM
                 │
                 ▼
       Encrypted Transaction
                 │
                 ▼
      Forwarding Simulation
                 │
                 ▼
       Next Processing Layer
```

---

## Cryptographic Components

### Scrypt

Scrypt is used for password-based key derivation.

A fresh random salt is generated for each encrypted transaction.

The implementation derives a 256-bit key for AES-GCM.

### AES-GCM

AES-GCM provides authenticated encryption.

It protects:

- confidentiality of the transaction payload
- integrity of encrypted data
- authentication of the ciphertext

A fresh nonce is generated for every encryption operation.

---

## Transaction Pipeline

The primary implementation is located at:

```text
src/secure_transaction.py
```

The processing sequence is:

```text
User Credentials
       ↓
Authentication
       ↓
Transaction Validation
       ↓
Random Salt + Nonce
       ↓
Scrypt Key Derivation
       ↓
AES-GCM Encryption
       ↓
Encrypted Payload
       ↓
Forwarding Simulation
```

---

## Example

```python
from src.secure_transaction import SecureTransactionPipeline


pipeline = SecureTransactionPipeline(
    valid_user_credentials={
        "alice": "password123"
    }
)

result = pipeline.process_transaction(
    username="alice",
    password="password123",
    transaction_data="Alice transfers 10 units to Bob",
)

print(result["success"])
```

The transaction payload is encrypted before the simulated forwarding stage.

---

## Security Properties Demonstrated

The implementation demonstrates:

- password-based key derivation
- random salts
- random AES-GCM nonces
- authenticated encryption
- ciphertext integrity verification
- credential validation
- transaction-content validation
- failure on incorrect decryption credentials

Repeated encryption of identical plaintext produces different ciphertext because fresh random values are generated.

---

## Automated Tests

The pytest suite covers:

```text
✓ valid credential authentication
✓ invalid credential rejection
✓ transaction validation
✓ AES-GCM encryption/decryption
✓ incorrect-password decryption failure
✓ fresh salt and nonce generation
✓ forwarding simulation
✓ complete transaction pipeline
✓ invalid pipeline credentials
✓ empty transaction rejection
```

Run:

```bash
pytest -v
```

---

## Original Research Notebooks

The repository preserves the original experimental notebooks under:

```text
notebooks/
```

They are retained as research history.

The production-style implementation in:

```text
src/
```

should be considered the primary implementation.

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Authenticated Encryption | AES-GCM |
| Key Derivation | Scrypt |
| Cryptography Library | Python `cryptography` |
| Testing | pytest |
| CI | GitHub Actions |
| Research Environment | Jupyter Notebook |

---

## Repository Structure

```text
Secure-Blockchain-Transactions/
│
├── src/
│   ├── __init__.py
│   └── secure_transaction.py
│
├── tests/
│   ├── conftest.py
│   └── test_secure_transaction.py
│
├── notebooks/
│   ├── secure_transaction_pipeline.ipynb
│   └── cryptographic_validation_demo.ipynb
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

---

## Installation

Clone:

```bash
git clone https://github.com/Dr-AmitVishwakarma/Secure-Blockchain-Transactions.git
cd Secure-Blockchain-Transactions
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest -v
```

---

## What This Project Is Not

Despite originating from experiments associated with a repository previously named `Quantum`, this implementation should not be interpreted as:

- quantum computing
- quantum key distribution
- quantum encryption
- a post-quantum cryptographic implementation
- a production blockchain
- a cryptocurrency
- a production authentication system

The current implementation deliberately uses established conventional cryptographic primitives.

---

## Security Limitations

This repository is a research and portfolio prototype.

Among other limitations:

- credentials are represented using an in-memory demonstration store
- no production identity provider is integrated
- no blockchain node is connected
- no key-management service is used
- no hardware security module is used
- no network forwarding actually occurs
- no security audit has been performed

Do not use the prototype for protecting real financial or sensitive production transactions.

---

## Future Work

Potential extensions include:

- digital signatures
- blockchain transaction integration
- hardware-backed key management
- secure credential storage
- replay-attack protection
- transaction sequencing
- audit logging
- standardized post-quantum cryptography such as ML-KEM or ML-DSA
- comparative cryptographic benchmarking
- formal threat modelling

---

## License

MIT License.

---

## Disclaimer

This software is provided for research, education, and portfolio demonstration purposes.