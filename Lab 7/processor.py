
import re


def notes_needed(amount):
    if not isinstance(amount, str):
        raise ValueError("Amount must be a string.")

    amount = amount.strip()

    if not amount:
        raise ValueError("Amount cannot be empty.")

    # Accept plain numbers or correctly formatted comma-separated numbers
    if not re.fullmatch(r"\d+|\d{1,3}(?:,\d{3})+", amount):
        raise ValueError("Enter a valid positive whole-number amount.")

    amount_value = int(amount.replace(",", ""))

    if amount_value <= 0:
        raise ValueError("Amount must be greater than zero.")

    return amount_value // 100


def mask_card(card_number):
    if not isinstance(card_number, str):
        raise ValueError("Card number must be a string.")

    # Accept 16 digits with or without spaces
    if re.fullmatch(r"\d{16}", card_number):
        digits = card_number
    elif re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", card_number):
        digits = card_number.replace(" ", "")
    else:
        raise ValueError("Enter a valid 16-digit card number.")

    return "XXXX XXXX XXXX " + digits[-4:]


def average_withdrawal(amounts_csv):
    if not isinstance(amounts_csv, str):
        raise ValueError("Withdrawals must be provided as a string.")

    if not amounts_csv.strip():
        raise ValueError("Withdrawal list cannot be empty.")

    parts = amounts_csv.split(",")

    if any(not part.strip().isdigit() for part in parts):
        raise ValueError("All withdrawals must be positive whole numbers.")

    amounts = [int(part.strip()) for part in parts]

    if any(amount <= 0 for amount in amounts):
        raise ValueError("Withdrawals must be greater than zero.")

    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")

    try:
        result = notes_needed(user_input)
        print("Number of 100 Notes:", result)
    except ValueError as error:
        print("Invalid input:", error)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")

    try:
        result = mask_card(user_input)
        print("Masked Card:", result)
    except ValueError as error:
        print("Invalid input:", error)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")

    try:
        result = average_withdrawal(user_input)
        print("Average Withdrawal:", result)
    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()

