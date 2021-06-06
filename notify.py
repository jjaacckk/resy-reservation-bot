from discord_webhook import DiscordWebhook, DiscordEmbed


class Colors:
    failure = red = "FF3049"
    success = green = "00F492"
    blue = "89B5D9"
    pink = "F57EB8"


def discord_basic(url: str, content: str) -> bool:
    wh = DiscordWebhook(url=url, content=content)
    r = wh.execute()
    return r.ok


def discord_embed(url: str, title: str, description: str, color: str = Colors.blue) -> bool:
    webhook = DiscordWebhook(url=url)
    embed = DiscordEmbed(title=title, description=description, color=color)
    webhook.add_embed(embed)
    r = webhook.execute()
    return r.ok
