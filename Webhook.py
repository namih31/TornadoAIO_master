from discord_webhook import DiscordWebhook,DiscordEmbed


def wbhk_cook_zalando(brand,model,size,photo,url,tid):
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/953426582612107355/kyC-tj7VD-YNluN6ykBOOCv8n2Fb34bbQuK48PLZa2hk1rRZbJnbcT5ixZKYeEoOlk0-", username="Tornado")
    embed = DiscordEmbed(title="**Tornado Cooked :cloud_tornado:**",url=url,color=242424)
    embed.set_author(name="Tornado hurl",icon_url="https://i.postimg.cc/nrp4bcFK/tornado-AIO-1.png")
    embed.set_footer(text="tornado notification")
    embed.add_embed_field(name='Brand',value=brand,inline=True)
    embed.add_embed_field(name='Model', value=model,inline=True)
    embed.add_embed_field(name='Size', value=size, inline= False)
    embed.add_embed_field(name='Site', value='Zalando')
    embed.add_embed_field(name='Task', value= tid)

    embed.set_thumbnail(url=photo)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    return

def wbhk_zalando(name,url,skus,size,stock,img,allsizes):
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/957069346516123649/GweTgzllHyAGBRYB8SVK99I5WPiz0vSlUEThFRHtTOX63s6ZoRiKHUdmpPIXobg9aDn3", username="Tornado")
    embed = DiscordEmbed(title= name,url=url,color=242424)
    embed.set_author(name="Tornado hurl",icon_url="https://i.postimg.cc/nrp4bcFK/tornado-AIO-1.png")
    embed.set_footer(text="tornado notification")
    embed.set_thumbnail(url=img)
    embed.add_embed_field(name="PID :athletic_shoe:", value=skus, inline=True)
    embed.add_embed_field(name="SIZE :straight_ruler:", value=size, inline=True)
    embed.add_embed_field(name="STOCK :globe_with_meridians:", value=stock, inline=True)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    wbhk_zalando_sizes(allsizes,name,url)
    return

def wbhk_zalando_cook_personal(brand, model, size, photo, url, tid,webhook_personal_url):
    webhook = DiscordWebhook(
        url=webhook_personal_url,
        username="Tornado")
    embed = DiscordEmbed(title="**Tornado Cooked :cloud_tornado:**", url=url, color=242424)
    embed.set_author(name="Tornado hurl", icon_url="https://i.postimg.cc/nrp4bcFK/tornado-AIO-1.png")
    embed.set_footer(text="tornado notification")
    embed.add_embed_field(name='Brand', value=brand, inline=True)
    embed.add_embed_field(name='Model', value=model, inline=True)
    embed.add_embed_field(name='Size', value=size, inline=False)
    embed.add_embed_field(name='Site', value='||Zalando||')
    embed.add_embed_field(name='Task', value="||"+ str(tid)+"||")

    embed.set_thumbnail(url=photo)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    return

def wbhk_zalando_sizes(allsizes,name,url):
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/957069346516123649/GweTgzllHyAGBRYB8SVK99I5WPiz0vSlUEThFRHtTOX63s6ZoRiKHUdmpPIXobg9aDn3", username="Tornado")
    embed = DiscordEmbed(title= name,url=url,color=242424)
    embed.set_footer(text="tornado notification")
    embed.add_embed_field(name='All Pids :pencil:',value=allsizes)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    return