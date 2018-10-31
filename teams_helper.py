import requests

def teams_message(message, channel, colour, image=False):
    """sends a card on teams"""
    card={
        "@context": "http://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": colour,
        "title": "Automated DrillBit analysis",
        "text": message
    }
    if image:
        card['text']+=" - [Click here for image](%s)" % image
    wh_resp=requests.post(url=channel, json=card)
    if wh_resp.status_code != 200:
        print(wh_resp.text)
