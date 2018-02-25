from passlib.totp import generate_secret
from datetime import datetime

secret = generate_secret()

dt = datetime.today().strftime("%Y-%m-%d")
output = ":".join([dt,secret])
print(output)

f = open("secret.txt","a")

f.write(output + "\n")


