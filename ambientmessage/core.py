"""
AM Core interaction with Inkyphat:

    - Display text
    - Display image (FIXME)

TODO:
    - Factorize MQTT client logic here: mqtt_subscribe(), mqtt_publish()
"""

import inky
import PIL, PIL.ImageFont, PIL.ImageDraw
import font_fredoka_one
import requests
import io
import logging

log = logging.getLogger(__name__)

inky_display = inky.auto()

def display(img, border=inky_display.BLACK):
    inky_display.set_border(border)
    inky_display.set_image(img)
    inky_display.show()

def display_text(message):
    font = PIL.ImageFont.truetype(font_fredoka_one.FredokaOne, 24)
    img = PIL.Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = PIL.ImageDraw.Draw(img)
    w, h = font.getsize(max(message.split('\n')))  # Fix take newlines into account
    h = h * (1.5 + message.count('\n'))              # Fix take newlines into account
    x = (inky_display.WIDTH / 2) - (w / 2)
    y = (inky_display.HEIGHT / 2) - (h / 2)
    # x = y = 10
    log.debug(f'Creating text: size=({w},{h}) display=({inky_display.WIDTH},{inky_display.HEIGHT}), message=({message})')
    draw.text((x, y), message, inky_display.BLACK, font)
    display(img)

def display_image(url):
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    img = PIL.Image.open(image_bytes)
    img = img.resize((inky_display.WIDTH, inky_display.HEIGHT), PIL.Image.Resampling.LANCZOS)
    # img.thumbnail((inky_display.WIDTH, inky_display.HEIGHT))
    display(img)

# display_image('https://avatars.githubusercontent.com/u/28109?s=200&v=4');
# display_text('Youhouu !')
