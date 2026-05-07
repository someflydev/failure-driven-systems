from opledger_api.db import database_target, sqlalchemy_database_url


def test_postgres_url_is_normalized_for_psycopg() -> None:
    assert (
        sqlalchemy_database_url("postgres://opledger@db.example.com:55432/opledger")
        == "postgresql+psycopg://opledger@db.example.com:55432/opledger"
    )


def test_postgresql_url_is_normalized_for_psycopg() -> None:
    assert (
        sqlalchemy_database_url("postgresql://opledger@db.example.com:55432/opledger")
        == "postgresql+psycopg://opledger@db.example.com:55432/opledger"
    )


def test_database_target_excludes_credentials() -> None:
    assert database_target("postgres://opledger@db.example.com:55432/opledger") == {
        "driver": "postgresql+psycopg",
        "host": "db.example.com",
        "port": 55432,
        "database": "opledger",
    }
