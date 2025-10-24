from app.core.security import generate_magic_token, decode_magic_token


def test_magic_token_roundtrip():
    token = generate_magic_token("test@example.com")
    email = decode_magic_token(token)
    assert email == "test@example.com"
