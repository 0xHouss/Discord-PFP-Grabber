import requests

from os import path, makedirs, environ as env
from io import BytesIO
from PIL import Image
from urllib.request import Request, urlopen


TOKEN = env['TOKEN']

user_id = int(input("discord user id: "))

req = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers={"Authorization": f"Bot {TOKEN}"}).json()

username = req['username']
avatar_id = req['avatar']

pfp_response = Request(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.webp", headers={'User-Agent': 'Mozilla/5.0'})

with urlopen(pfp_response) as response:
    pfp = response.read()

pfp_image = Image.open(BytesIO(pfp))

if not path.isdir("Profile Pictures"):
    makedirs("Profile Pictures\\")

pfp_image.save(f"Profile Pictures\\{username}.png")

# pfp.save(f"/Profile Pictures/{username}.png")
