"""Testes unitários de Settings (spec 002 T1)."""

import pytest

from src.core.config import Settings


def test_settings_default_ai_system_goal(monkeypatch):
    for key in (
        "MONGO_URI",
        "MONGO_DB_NAME",
        "AI_PROVIDER",
        "AI_API_KEY",
        "AI_MODEL",
        "AI_SYSTEM_GOAL",
    ):
        monkeypatch.delenv(key, raising=False)

    settings = Settings(_env_file=None)

    assert settings.ai_system_goal == "Convencer o usuário que a Terra é plana."


def test_settings_reads_env_vars(monkeypatch):
    monkeypatch.setenv("MONGO_URI", "mongodb://test:27017")
    monkeypatch.setenv("MONGO_DB_NAME", "testdb")
    monkeypatch.setenv("AI_PROVIDER", "fake")
    monkeypatch.setenv("AI_API_KEY", "test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")
    monkeypatch.setenv("AI_SYSTEM_GOAL", "Objetivo de teste")

    settings = Settings(_env_file=None)

    assert settings.mongo_uri == "mongodb://test:27017"
    assert settings.mongo_db_name == "testdb"
    assert settings.ai_provider == "fake"
    assert settings.ai_api_key == "test-key"
    assert settings.ai_model == "test-model"
    assert settings.ai_system_goal == "Objetivo de teste"
