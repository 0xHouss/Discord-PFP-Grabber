import requests

from os import path, makedirs, environ as env
from io import BytesIO
from PIL import Image
from urllib.request import Request, urlopen



TOKEN = env['TOKEN']

user_id = int(input("discord user id: "))

username = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers={"Authorization": f"Bot {TOKEN}"}).json()['username']

avatar_id = requests.get(f'https://discord.com/api/v9/users/{user_id}', headers={"Authorization": f"Bot {TOKEN}"}).json()['avatar']

req = Request(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.webp", headers={'User-Agent': 'Mozilla/5.0'})

with urlopen(req) as u:
    raw_data = u.read()

pfp = Image.open(BytesIO(raw_data))

if not path.isdir("Profile Pictures"):
    makedirs("Profile Pictures\\")

pfp.save(f"Profile Pictures\\{username}.png")

# pfp.save(f"/Profile Pictures/{username}.png")
