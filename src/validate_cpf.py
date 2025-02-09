CPF_LENGTH = 11

def validate_cpf(cpf: str) -> bool:
    """
    Validates CPF
    """
    if not cpf:
        return False
    
    cpf = clean(cpf)
    if len(cpf) != CPF_LENGTH:
        return False
    
    if all_digits_are_the_same(cpf):
        return False
    
    digit1 = calculate_digit(cpf, 10)
    digit2 = calculate_digit(cpf, 11)
    
    return extract_digit(cpf) == f"{digit1}{digit2}"

def clean(cpf: str) -> str:
    """
    Cleans special characters from the CPF
    """
    return ''.join([char for char in cpf if char.isdigit()])

def all_digits_are_the_same(cpf: str) -> bool:
    """
    Checks if all digits are the same
    """
    return cpf[0] * len(cpf) == cpf

def calculate_digit(cpf: str, factor: int) -> int:
    """
    Considers only the first 9 digits for calculation
    """
    total = 0
    for i, digit in enumerate(cpf[:9]):  
        total += int(digit) * (factor - i)
    rest = total % 11
    return 0 if rest < 2 else 11 - rest

def extract_digit(cpf: str) -> str:
    """
    Extrai os 2 últimos dígitos
    """
    return cpf[-2:]  
