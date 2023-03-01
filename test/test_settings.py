from settings import Settings


def test_settings_parses_csv_origins():
    settings = Settings(origin_str="http://localhost:3000,http://localhost")
    assert settings.origins == ["http://localhost:3000", "http://localhost"]
