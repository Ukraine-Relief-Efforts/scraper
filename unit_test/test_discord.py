from pathlib import Path

import pytest

from utils.utils import DiscordLogData, LogLevelEnum, log_to_discord


@pytest.fixture
def hook(fs):
    path = Path(__file__).parent.parent / "src" / "utils" / ".discord-webhook"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("https://www.example.com/discord")


@pytest.fixture
def simple_data():
    return DiscordLogData(
        title="MyTitle", description="MyDesc", log_level=LogLevelEnum.ERROR
    )


def test_log_to_discord_calls_post(hook, mrpost, simple_data):
    log_to_discord([simple_data])
    assert mrpost.called


def test_log_to_discord_without_config_does_not_raise(mrpost, simple_data):
    log_to_discord([simple_data])
    assert not mrpost.called


def test_log_to_discord_with_too_many_entries_does_not_log(hook, mrpost, simple_data):
    log_to_discord([simple_data for _ in range(11)] * 11)
    assert not mrpost.called

def test_fail():
    # TODO: Remove this failing test (I'm messing with the CI)
    assert False
