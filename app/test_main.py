from collections.abc import Callable

import pytest

from app.main import check_password


@pytest.fixture(scope="module")
def check() -> Callable[[str], bool]:
    return check_password


class TestLength:
    @pytest.mark.parametrize(
        "password",
        [
            "Abc1!de",
            "Abcdefghijk1!lmno",
        ],
        ids=[
            "too short (7 chars)",
            "too long (17 chars)",
        ],
    )
    def test_rejects_if_length_out_of_bounds(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is False

    @pytest.mark.parametrize(
        "password",
        [
            "Abc1!def",
            "Abcdef1!ghijKlm",
        ],
        ids=[
            "min length (8 chars)",
            "max length (16 chars)",
        ],
    )
    def test_accepts_if_length_within_bounds(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is True


class TestRequiredParts:
    @pytest.mark.parametrize(
        "password",
        [
            "abcdef1!",
        ],
        ids=[
            "missing uppercase",
        ],
    )
    def test_rejects_without_uppercase(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is False

    @pytest.mark.parametrize(
        "password",
        [
            "Abcdefg!",
        ],
        ids=[
            "missing digit",
        ],
    )
    def test_rejects_without_digit(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is False

    @pytest.mark.parametrize(
        "password",
        [
            "Abcdefg1",
        ],
        ids=[
            "missing special character",
        ],
    )
    def test_rejects_without_special_char(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is False

    def test_accepts_with_all_required_parts(
        self,
        check: Callable[[str], bool],
    ) -> None:
        assert check("GoodP@ss1") is True


class TestAllowedCharacters:
    @pytest.mark.parametrize(
        "password",
        [
            "Valid1! ",
            "Valid1!Ж",
            "Valid1!.com",
            "Valid1!🙂",
        ],
        ids=[
            "space character",
            "cyrillic 'Ж'",
            "dot character",
            "emoji",
        ],
    )
    def test_rejects_with_invalid_characters(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is False

    @pytest.mark.parametrize(
        "password",
        [
            "Val1$dPas",
            "Go@dPass1",
            "Pass#Word1",
            "Abc&def1!",
            "Hey-You1!",
            "Val_id1!",
            "Yes!Go1#",
        ],
        ids=[
            "contains '$'",
            "contains '@'",
            "contains '#'",
            "contains '&'",
            "contains '-'",
            "contains '_'",
            "contains '!' and '#'",
        ],
    )
    def test_accepts_with_valid_special_characters(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is True


class TestValidCases:
    @pytest.mark.parametrize(
        "password",
        [
            "Pass@word1",
            "A1!bcdefg",
            "Good#Pass1234",
            "ABcd12!@",
        ],
    )
    def test_accepts_valid_passwords(
        self,
        check: Callable[[str], bool],
        password: str,
    ) -> None:
        assert check(password) is True
