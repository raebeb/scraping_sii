from rut_chile import rut_chile


def validate_rut(rut: str) -> bool:
    return rut_chile.is_valid_rut(rut)


def rut_to_dict(rut: str) -> dict:
    rut_without_digit = rut_chile.format_rut_without_dots(rut)[:-2]

    return {
        "rut": rut_without_digit,
        "dv": rut_chile.get_verification_digit(rut_without_digit),
        "rutcntr": rut_chile.format_capitalized_rut_with_dots(rut),
    }
