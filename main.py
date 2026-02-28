import datetime
import discord
from discord.ext import commands
import os

# Botun çalışması için gerekli intent'ler
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Üye bilgilerine erişmek için

# Bot nesnesi, komut öneki "m+" olarak ayarlandı
bot = commands.Bot(command_prefix="m+", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")

# KICK KOMUTU
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Belirtilmedi"):
    """Belirtilen üyeyi sunucudan atar."""
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} sunucudan atıldı. Sebep: {reason}")

# BAN KOMUTU
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Belirtilmedi"):
    """Belirtilen üyeyi sunucudan yasaklar."""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} yasaklandı. Sebep: {reason}")

# UNBAN KOMUTU (Kullanıcı ID'si ile)
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int, *, reason="Belirtilmedi"):
    """ID'si verilen kullanıcının yasağını kaldırır."""
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user, reason=reason)
    await ctx.send(f"{user.name} (#{user.discriminator}) kullanıcısının yasağı kaldırıldı.")

# SUSTURMA (MUTE) KOMUTU - Discord'un timeout özelliğini kullanır
@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason="Belirtilmedi"):
    """
    Belirtilen üyeyi geçici olarak susturur.
    Kullanım: m+mute @kullanıcı dakika [sebep]
    Örnek: m+mute @ahmet 10 Çok konuşuyor
    """
    # Süreyi saniyeye çevir (discord.Timeout: saniye cinsinden)
    timeout_duration = duration * 60  # dakika * 60 = saniye
    await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=timeout_duration), reason=reason)
    await ctx.send(f"{member.mention} susturuldu. Süre: {duration} dakika. Sebep: {reason}")

# Hata yakalama (yetki yoksa)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu kullanmak için yeterli yetkiniz yok.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Hatalı argüman. Lütfen doğru kullanımı kontrol edin.")
    else:
        raise error  # Diğer hataları göster

# Token'ı çevre değişkeninden al
bot.run(os.getenv("DISCORD_TOKEN"))
