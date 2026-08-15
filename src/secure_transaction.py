from __future__ import annotations

import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


@dataclass(frozen=True)
class EncryptedTransaction:
    salt: bytes
    nonce: bytes
    ciphertext: bytes


class SecureTransactionPipeline:
    """
    Demonstration pipeline for encrypting, decrypting,
    validating, and forwarding blockchain-oriented
    transaction payloads.

    This module uses conventional cryptography:
    - Scrypt for password-based key derivation
    - AES-GCM for authenticated encryption

    It is not a quantum-computing or post-quantum
    cryptography implementation.
    """

    KEY_LENGTH = 32
    SALT_LENGTH = 16
    NONCE_LENGTH = 12

    def __init__(
        self,
        valid_user_credentials: dict[str, str],
    ) -> None:
        self.valid_user_credentials = (
            valid_user_credentials.copy()
        )

    def validate_user(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Validate a username/password pair against the
        configured demonstration credential store.
        """

        expected_password = (
            self.valid_user_credentials.get(
                username
            )
        )

        return (
            expected_password is not None
            and expected_password == password
        )

    @staticmethod
    def _derive_key(
        password: str,
        salt: bytes,
    ) -> bytes:
        """
        Derive a 256-bit encryption key using Scrypt.
        """

        if not password:
            raise ValueError(
                "Password must not be empty."
            )

        if not salt:
            raise ValueError(
                "Salt must not be empty."
            )

        kdf = Scrypt(
            salt=salt,
            length=(
                SecureTransactionPipeline
                .KEY_LENGTH
            ),
            n=2**14,
            r=8,
            p=1,
        )

        return kdf.derive(
            password.encode("utf-8")
        )

    def encrypt_transaction(
        self,
        transaction_data: str,
        password: str,
    ) -> EncryptedTransaction:
        """
        Encrypt transaction text using AES-GCM.

        A fresh random salt and nonce are generated for
        each encrypted transaction.
        """

        if not transaction_data:
            raise ValueError(
                "Transaction data must not be empty."
            )

        salt = os.urandom(
            self.SALT_LENGTH
        )

        nonce = os.urandom(
            self.NONCE_LENGTH
        )

        key = self._derive_key(
            password=password,
            salt=salt,
        )

        cipher = AESGCM(
            key
        )

        ciphertext = cipher.encrypt(
            nonce,
            transaction_data.encode(
                "utf-8"
            ),
            None,
        )

        return EncryptedTransaction(
            salt=salt,
            nonce=nonce,
            ciphertext=ciphertext,
        )

    def decrypt_transaction(
        self,
        encrypted_transaction: (
            EncryptedTransaction
        ),
        password: str,
    ) -> str:
        """
        Decrypt and authenticate an encrypted transaction.
        """

        key = self._derive_key(
            password=password,
            salt=(
                encrypted_transaction
                .salt
            ),
        )

        cipher = AESGCM(
            key
        )

        plaintext = cipher.decrypt(
            encrypted_transaction.nonce,
            encrypted_transaction.ciphertext,
            None,
        )

        return plaintext.decode(
            "utf-8"
        )

    @staticmethod
    def validate_transaction(
        transaction_data: str,
    ) -> bool:
        """
        Perform lightweight transaction validation.

        The current demonstration requires non-empty
        transaction content after whitespace removal.
        """

        return bool(
            transaction_data.strip()
        )

    @staticmethod
    def forward_to_next_layer(
        encrypted_transaction: (
            EncryptedTransaction
        ),
    ) -> dict[str, object]:
        """
        Simulate forwarding an encrypted payload to the
        next processing layer.

        No network communication occurs.
        """

        return {
            "status": "forwarded",
            "payload_size_bytes": len(
                encrypted_transaction
                .ciphertext
            ),
        }

    def process_transaction(
        self,
        username: str,
        password: str,
        transaction_data: str,
    ) -> dict[str, object]:
        """
        Run the complete demonstration pipeline:
        authentication -> validation -> encryption ->
        forwarding.
        """

        if not self.validate_user(
            username=username,
            password=password,
        ):
            return {
                "success": False,
                "reason": (
                    "invalid_credentials"
                ),
            }

        if not self.validate_transaction(
            transaction_data
        ):
            return {
                "success": False,
                "reason": (
                    "invalid_transaction"
                ),
            }

        encrypted = (
            self.encrypt_transaction(
                transaction_data=(
                    transaction_data
                ),
                password=password,
            )
        )

        forwarding_result = (
            self.forward_to_next_layer(
                encrypted
            )
        )

        return {
            "success": True,
            "encrypted_transaction": (
                encrypted
            ),
            "forwarding": (
                forwarding_result
            ),
        }