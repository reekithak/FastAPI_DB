import os

path = os.getenv("Path")
print(os.getenv("USERNAME"))
var_dict = {
    "USERNAME": "postgres",
    "PASSWORD": "123456",
    "SECRET_KEY": "09bhdfgvdhfdbn873bgv784bhb4802ub3h4888230",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 100,
}

for name, value in var_dict.items():
    os.system(f"conda env config vars set {name}={value}")

os.system("conda env config vars list")
