import random

characters = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


password_length = int(input("Введите желаемую длину пароля: "))

generated_password = ""

for _ in range(password_length):
    random_character = random.choice(characters)
    generated_password += random_character

print("Сгенерированный пароль:", generated_password)
