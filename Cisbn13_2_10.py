def isbn13_to_isbn10(isbn13):
    # Remove dashes or spaces if present in the ISBN-13
    isbn13 = isbn13.replace("-", "").replace(" ", "")

    # Ensure that the input is a valid ISBN-13
    if len(isbn13) != 13 or not isbn13.isdigit():
        raise ValueError("Invalid ISBN-13 format")

    # Take the first 9 digits of the ISBN-13
    first_9_digits = isbn13[3:12]

    # Calculate the checksum digit (the last digit of the ISBN-10)
    checksum = 0
    for i in range(9):
        checksum += int(first_9_digits[i]) * (10 - i)
    checksum = (11 - (checksum % 11)) % 11

    # Convert the checksum digit to a character
    if checksum == 10:
        checksum = "X"

    # Create the ISBN-10 by combining the first 9 digits and the checksum
    isbn10 = first_9_digits + str(checksum)

    return isbn10


# Input and output file paths
input_file = "isbn-ja2.txt"  # Replace with the path to your input file
output_file = "isbn-ja2-isbn10.csv"  # Replace with the path to your output file

# Read ISBN-13 numbers from the input file and convert them to ISBN-10
with open(input_file, "r") as input_file:
    isbn13_numbers = [line.strip() for line in input_file]

isbn10_numbers = [isbn13_to_isbn10(isbn13) for isbn13 in isbn13_numbers]

isbn10_numbers.insert(0, 'ISBN')

# Write the converted ISBN-10 numbers to the output file
with open(output_file, "w") as output_file:
    for isbn10 in isbn10_numbers:
        output_file.write(isbn10 + "\n")

print(f"Conversion completed. ISBN-10 numbers saved to {output_file}")