import pytest

from src.secure_transaction import (
    EncryptedTransaction,
    SecureTransactionPipeline,
)


@pytest.fixture
def pipeline():
    return SecureTransactionPipeline(
        valid_user_credentials={
            "alice": "password123",
            "bob": "secure456",
        }
    )


def test_valid_user_credentials(
    pipeline,
):
    assert (
        pipeline.validate_user(
            "alice",
            "password123",
        )
        is True
    )


def test_invalid_user_credentials(
    pipeline,
):
    assert (
        pipeline.validate_user(
            "alice",
            "wrong-password",
        )
        is False
    )


def test_transaction_validation(
    pipeline,
):
    assert (
        pipeline.validate_transaction(
            "transfer 10 units"
        )
        is True
    )

    assert (
        pipeline.validate_transaction(
            "   "
        )
        is False
    )


def test_encrypt_and_decrypt_transaction(
    pipeline,
):
    plaintext = (
        "Alice transfers 10 units to Bob"
    )

    encrypted = (
        pipeline.encrypt_transaction(
            transaction_data=plaintext,
            password="password123",
        )
    )

    assert isinstance(
        encrypted,
        EncryptedTransaction,
    )

    assert (
        encrypted.ciphertext
        != plaintext.encode("utf-8")
    )

    decrypted = (
        pipeline.decrypt_transaction(
            encrypted_transaction=(
                encrypted
            ),
            password="password123",
        )
    )

    assert decrypted == plaintext


def test_wrong_password_cannot_decrypt(
    pipeline,
):
    encrypted = (
        pipeline.encrypt_transaction(
            transaction_data=(
                "confidential transaction"
            ),
            password="password123",
        )
    )

    with pytest.raises(
        Exception
    ):
        pipeline.decrypt_transaction(
            encrypted_transaction=(
                encrypted
            ),
            password="wrong-password",
        )


def test_encryption_uses_fresh_random_values(
    pipeline,
):
    payload = (
        "same transaction"
    )

    first = (
        pipeline.encrypt_transaction(
            payload,
            "password123",
        )
    )

    second = (
        pipeline.encrypt_transaction(
            payload,
            "password123",
        )
    )

    assert first.salt != second.salt

    assert first.nonce != second.nonce

    assert (
        first.ciphertext
        != second.ciphertext
    )


def test_forwarding_simulation(
    pipeline,
):
    encrypted = (
        pipeline.encrypt_transaction(
            transaction_data=(
                "transaction"
            ),
            password="password123",
        )
    )

    result = (
        pipeline.forward_to_next_layer(
            encrypted
        )
    )

    assert (
        result["status"]
        == "forwarded"
    )

    assert (
        result[
            "payload_size_bytes"
        ]
        > 0
    )


def test_full_pipeline_success(
    pipeline,
):
    result = (
        pipeline.process_transaction(
            username="alice",
            password="password123",
            transaction_data=(
                "Alice transfers 10 units"
            ),
        )
    )

    assert (
        result["success"]
        is True
    )

    assert (
        result["forwarding"][
            "status"
        ]
        == "forwarded"
    )


def test_full_pipeline_rejects_bad_credentials(
    pipeline,
):
    result = (
        pipeline.process_transaction(
            username="alice",
            password="wrong",
            transaction_data=(
                "Alice transfers 10 units"
            ),
        )
    )

    assert (
        result["success"]
        is False
    )

    assert (
        result["reason"]
        == "invalid_credentials"
    )


def test_full_pipeline_rejects_empty_transaction(
    pipeline,
):
    result = (
        pipeline.process_transaction(
            username="alice",
            password="password123",
            transaction_data="",
        )
    )

    assert (
        result["success"]
        is False
    )

    assert (
        result["reason"]
        == "invalid_transaction"
    )