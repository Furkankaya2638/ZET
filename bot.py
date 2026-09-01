import os
import threading
from datetime import timedelta

import discord
from discord.ext import commands
from flask import Flask, render_template_string, request, redirect


# =========================================================
# ZET BOT
# =========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

app = Flask(__name__)


# =========================================================
# AYARLAR
# =========================================================

ayarlar = {
    "karsilama": True,
    "ayrilma": False,
    "moderasyon": True,
    "guvenlik": True,
    "loglar": True,
}


# =========================================================
# PANEL TASARIMI
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ZET Yönetim Paneli</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background:
        radial-gradient(circle at top left, #4c1d95, transparent 30%),
        radial-gradient(circle at top right, #1d4ed8, transparent 30%),
        #070914;
    color: white;
}

.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100vh;
    padding: 25px 15px;
    background: rgba(5, 8, 20, .97);
    border-right: 1px solid #252b42;
}

.logo {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;
    color: #a78bfa;
}

.sunucu {
    padding: 15px;
    background: #11162a;
    border-radius: 12px;
    margin-bottom: 25px;
}

.baslik {
    color: #68748f;
    font-size: 11px;
    margin: 20px 8px 8px;
}

.menu a {
    display: block;
    padding: 12px;
    margin: 5px 0;
    color: #cbd5e1;
    text-decoration: none;
    border-radius: 9px;
}

.menu a:hover {
    background: #312e81;
    color: white;
}

.ana {
    margin-left: 250px;
    padding: 35px;
}

.ust {
    margin-bottom: 30px;
}

h1 {
    margin: 0;
}

.aciklama {
    color: #8d97ae;
    margin-top: 8px;
}

.kartlar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 30px;
}

.kart {
    background: rgba(13, 18, 37, .95);
    border: 1px solid #252b42;
    border-radius: 16px;
    padding: 22px;
}

.kart-baslik {
    color: #8d97ae;
    font-size: 12px;
}

.kart-sayi {
    font-size: 27px;
    font-weight: bold;
    margin-top: 8px;
}

.sistemler {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.sistem {
    background: rgba(13, 18, 37, .95);
    border: 1px solid #252b42;
    border-radius: 16px;
    padding: 20px;
}

.sistem-baslik {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sistem h3 {
    margin: 0;
}

.sistem p {
    color: #8d97ae;
    min-height: 40px;
}

.buton {
    display: inline-block;
    padding: 10px 15px;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 9px;
    cursor: pointer;
}

.buton:hover {
    opacity: .85;
}

.switch {
    width: 52px;
    height: 28px;
    position: relative;
    display: inline-block;
}

.switch input {
    display: none;
}

.slider {
    position: absolute;
    inset: 0;
    background: #ef4444;
    border-radius: 30px;
    cursor: pointer;
}

.slider:before {
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    left: 4px;
    top: 4px;
    background: white;
    border-radius: 50%;
    transition: .2s;
}

.switch input:checked + .slider {
    background: #22c55e;
}

.switch input:checked + .slider:before {
    transform: translateX(24px);
}

.ayar {
    background: rgba(13,18,37,.95);
    border: 1px solid #252b42;
    border-radius: 16px;
    padding: 25px;
    max-width: 900px;
}

input[type=text],
textarea,
select {
    width: 100%;
    background: #080b16;
    color: white;
    border: 1px solid #30384e;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0 18px;
}

textarea {
    min-height: 130px;
}

@media(max-width: 1000px) {

    .kartlar {
        grid-template-columns: repeat(2, 1fr);
    }

    .sistemler {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media(max-width: 700px) {

    .sidebar {
        width: 190px;
    }

    .ana {
        margin-left: 190px;
        padding: 20px;
    }

    .kartlar,
    .sistemler {
        grid-template-columns: 1fr;
    }
}

</style>
</head>

<body>

<div class="sidebar">

    <div class="logo">🤖 ZET</div>

    <div class="sunucu">
        <small>SUNUCU</small><br>
        <strong>ZET Sunucun</strong>
    </div>

    <div class="baslik">GENEL</div>

    <div class="menu">
        <a href="/">🏠 Ana Sayfa</a>
        <a href="/yardim">📖 Yardım</a>
    </div>

    <div class="baslik">OTOMASYON</div>

    <div class="menu">
        <a href="/karsilama">👋 Karşılama</a>
        <a href="/ayrilma">🚪 Ayrılma</a>
    </div>

    <div class="baslik">SUNUCU</div>

    <div class="menu">
        <a href="/moderasyon">🛡️ Moderasyon</a>
        <a href="/guvenlik">🔒 Güvenlik</a>
        <a href="/loglar">📋 Loglar</a>
    </div>

    <div class="baslik">ARAÇLAR</div>

    <div class="menu">
        <a href="/istatistik">📊 İstatistik</a>
        <a href="/ayarlar">⚙️ Ayarlar</a>
    </div>

</div>


<div class="ana">

{% if sayfa == "ana" %}

<div class="ust">
    <h1>ZET Yönetim Paneli</h1>
    <div class="aciklama">
        Discord sunucunu buradan yönet.
    </div>
</div>

<div class="kartlar">

    <div class="kart">
        <div class="kart-baslik">BOT DURUMU</div>
        <div class="kart-sayi">ÇEVRİM İÇİ</div>
    </div>

    <div class="kart">
        <div class="kart-baslik">SUNUCU ÜYELERİ</div>
        <div class="kart-sayi">{{ uyeler }}</div>
    </div>

    <div class="kart">
        <div class="kart-baslik">AKTİF SİSTEMLER</div>
        <div class="kart-sayi">{{ aktif }}</div>
    </div>

    <div class="kart">
        <div class="kart-baslik">SUNUCU SAYISI</div>
        <div class="kart-sayi">{{ sunucular }}</div>
    </div>

</div>

<h2>ZET Sistemleri</h2>

<div class="sistemler">

{% for anahtar, bilgi in sistemler.items() %}

<div class="sistem">

    <div class="sistem-baslik">

        <h3>{{ bilgi["isim"] }}</h3>

        <form method="POST" action="/ac-kapat/{{ anahtar }}">

            <label class="switch">

                <input
                    type="checkbox"
                    onchange="this.form.submit()"
                    {% if ayarlar[anahtar] %}checked{% endif %}
                >

                <span class="slider"></span>

            </label>

        </form>

    </div>

    <p>
        {{ bilgi["aciklama"] }}
    </p>

    <a class="buton" href="/{{ anahtar }}">
        Ayarları Aç
    </a>

</div>

{% endfor %}

</div>


{% elif sayfa == "yardim" %}

<h1>📖 Yardım</h1>

<div class="ayar">

<h2>ZET Kullanımı</h2>

<p>
Bu panel üzerinden ZET botunun sistemlerini yönetebilirsin.
</p>

<p>
Ana sayfadan sistemleri açıp kapatabilirsin.
</p>

</div>


{% elif sayfa == "istatistik" %}

<h1>📊 İstatistik</h1>

<div class="kartlar">

<div class="kart">
<div class="kart-baslik">SUNUCU</div>
<div class="kart-sayi">{{ sunucular }}</div>
</div>

<div class="kart">
<div class="kart-baslik">TOPLAM ÜYE</div>
<div class="kart-sayi">{{ uyeler }}</div>
</div>

<div class="kart">
<div class="kart-baslik">AKTİF SİSTEM</div>
<div class="kart-sayi">{{ aktif }}</div>
</div>

</div>


{% elif sayfa in ["karsilama", "ayrilma"] %}

<h1>
{% if sayfa == "karsilama" %}
👋 Karşılama
{% else %}
🚪 Ayrılma
{% endif %}
</h1>

<br>

<div class="ayar">

<form method="POST" action="/kaydet/{{ sayfa }}">

<label>Sistem Durumu</label>

<br><br>

<label class="switch">

<input
type="checkbox"
name="aktif"
{% if ayarlar[sayfa] %}checked{% endif %}
>

<span class="slider"></span>

</label>

<br><br>

<label>Kanal</label>

<select name="kanal">

<option>#hos-geldin</option>
<option>#genel</option>
<option>#duyurular</option>

</select>

<label>Mesaj</label>

<textarea name="mesaj">{% if sayfa == "karsilama" %}👋 Hoş geldin {uye}! Sunucumuzda artık {uyesayisi} kişiyiz!{% else %}🚪 {uye} sunucudan ayrıldı. Sunucumuzda artık {uyesayisi} kişiyiz.{% endif %}</textarea>

<button class="buton" type="submit">
💾 Kaydet
</button>

</form>

</div>


{% else %}

<h1>{{ baslik }}</h1>

<br>

<div class="ayar">

<h2>{{ baslik }} Ayarları</h2>

<p>
Bu bölüm ZET yönetim panelinden yönetilir.
</p>

<form method="POST" action="/ac-kapat/{{ anahtar }}">

<button class="buton" type="submit">
{% if ayarlar.get(anahtar, False) %}
Sistemi Kapat
{% else %}
Sistemi Aç
{% endif %}
</button>

</form>

</div>

{% endif %}

</div>

</body>
</html>
"""


# =========================================================
# SİSTEMLER
# =========================================================

sistemler = {

    "karsilama": {
        "isim": "👋 Karşılama",
        "aciklama": "Sunucuya yeni gelen üyeleri karşılar."
    },

    "ayrilma": {
        "isim": "🚪 Ayrılma",
        "aciklama": "Sunucudan ayrılan üyeleri bildirir."
    },

    "moderasyon": {
        "isim": "🛡️ Moderasyon",
        "aciklama": "Ban, kick, timeout ve mesaj temizleme."
    },

    "guvenlik": {
        "isim": "🔒 Güvenlik",
        "aciklama": "Sunucunun güvenlik ayarlarını yönet."
    },

    "loglar": {
        "isim": "📋 Loglar",
        "aciklama": "Sunucu işlemlerini takip et."
    }
}


# =========================================================
# PANEL VERİLERİ
# =========================================================

def panel_verisi():

    uyeler = sum(
        guild.member_count or 0
        for guild in bot.guilds
    )

    return {
        "ayarlar": ayarlar,
        "sistemler": sistemler,
        "uyeler": uyeler,
        "sunucular": len(bot.guilds),
        "aktif": sum(
            1 for x in ayarlar.values()
            if x
        )
    }


# =========================================================
# ANA SAYFA
# =========================================================

@app.route("/")
def ana_sayfa():

    veri = panel_verisi()

    veri["sayfa"] = "ana"

    return render_template_string(
        HTML,
        **veri
    )


# =========================================================
# SİSTEM AÇ / KAPAT
# =========================================================

@app.route(
    "/ac-kapat/<anahtar>",
    methods=["POST"]
)
def ac_kapat(anahtar):

    if anahtar in ayarlar:

        ayarlar[anahtar] = not ayarlar[anahtar]

    return redirect(
        request.referrer or "/"
    )


# =========================================================
# KARŞILAMA / AYRILMA AYARLARI
# =========================================================

mesajlar = {

    "karsilama":
        "👋 Hoş geldin {uye}! Sunucumuzda artık {uyesayisi} kişiyiz!",

    "ayrilma":
        "🚪 {uye} sunucudan ayrıldı. Sunucumuzda artık {uyesayisi} kişiyiz."
}


@app.route("/kaydet/<sayfa>", methods=["POST"])
def kaydet(sayfa):

    if sayfa in ayarlar:

        ayarlar[sayfa] = "aktif" in request.form

    if sayfa in mesajlar:

        mesajlar[sayfa] = request.form.get(
            "mesaj",
            mesajlar[sayfa]
        )

    return redirect(
        "/" + sayfa
    )


@app.route("/karsilama")
def karsilama():

    veri = panel_verisi()
    veri["sayfa"] = "karsilama"

    return render_template_string(
        HTML,
        **veri
    )


@app.route("/ayrilma")
def ayrilma():

    veri = panel_verisi()
    veri["sayfa"] = "ayrilma"

    return render_template_string(
        HTML,
        **veri
    )


# =========================================================
# DİĞER SAYFALAR
# =========================================================

@app.route("/<sayfa>")
def diger_sayfa(sayfa):

    if sayfa not in sistemler:

        if sayfa == "yardim":

            veri = panel_verisi()
            veri["sayfa"] = "yardim"

            return render_template_string(
                HTML,
                **veri
            )

        if sayfa == "istatistik":

            veri = panel_verisi()
            veri["sayfa"] = "istatistik"

            return render_template_string(
                HTML,
                **veri
            )

        if sayfa == "ayarlar":

            veri = panel_verisi()
            veri["sayfa"] = "ayarlar"
            veri["baslik"] = "⚙️ Ayarlar"
            veri["anahtar"] = "ayarlar"

            return render_template_string(
                HTML,
                **veri
            )

        return "Sayfa bulunamadı", 404

    veri = panel_verisi()

    veri["sayfa"] = "diger"
    veri["baslik"] = sistemler[sayfa]["isim"]
    veri["anahtar"] = sayfa

    return render_template_string(
        HTML,
        **veri
    )


# =========================================================
# DISCORD
# =========================================================

@bot.event
async def on_ready():

    print("")
    print("==============================")
    print("🤖 ZET AKTİF")
    print(f"👤 Bot: {bot.user}")
    print(f"🌐 Sunucu: {len(bot.guilds)}")
    print("==============================")


# =========================================================
# /YARDIM
# =========================================================

@bot.tree.command(
    name="yardim",
    description="ZET yardım menüsünü gösterir."
)
async def yardim(interaction):

    embed = discord.Embed(
        title="🤖 ZET Yardım",
        description="ZET botunun Türkçe komutları:",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="📖 Genel",
        value=(
            "`/yardim`\n"
            "`/sunucu`\n"
            "`/kullanici`\n"
            "`/avatar`\n"
            "`/istatistik`"
        ),
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderasyon",
        value=(
            "`/ban`\n"
            "`/kick`\n"
            "`/timeout`\n"
            "`/temizle`"
        ),
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )


# =========================================================
# /SUNUCU
# =========================================================

@bot.tree.command(
    name="sunucu",
    description="Sunucu bilgilerini gösterir."
)
async def sunucu(interaction):

    guild = interaction.guild

    if guild is None:

        await interaction.response.send_message(
            "❌ Bu komut sadece sunucuda kullanılabilir."
        )

        return

    embed = discord.Embed(
        title=f"🏠 {guild.name}",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="👥 Üye",
        value=str(guild.member_count),
        inline=True
    )

    embed.add_field(
        name="💬 Kanal",
        value=str(len(guild.channels)),
        inline=True
    )

    embed.add_field(
        name="🎭 Rol",
        value=str(len(guild.roles)),
        inline=True
    )

    if guild.icon:

        embed.set_thumbnail(
            url=guild.icon.url
        )

    await interaction.response.send_message(
        embed=embed
    )


# =========================================================
# /KULLANICI
# =========================================================

@bot.tree.command(
    name="kullanici",
    description="Kullanıcı bilgilerini gösterir."
)
async def kullanici(
    interaction,
    uye: discord.Member = None
):

    uye = uye or interaction.user

    embed = discord.Embed(
        title=f"👤 {uye}",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="🆔 Kullanıcı ID",
        value=str(uye.id),
        inline=False
    )

    embed.add_field(
        name="📅 Hesap oluşturma",
        value=discord.utils.format_dt(
            uye.created_at,
            style="F"
        ),
        inline=False
    )

    embed.set_thumbnail(
        url=uye.display_avatar.url
    )

    await interaction.response.send_message(
        embed=embed
    )


# =========================================================
# /AVATAR
# =========================================================

@bot.tree.command(
    name="avatar",
    description="Kullanıcının avatarını gösterir."
)
async def avatar(
    interaction,
    uye: discord.Member = None
):

    uye = uye or interaction.user

    embed = discord.Embed(
        title=f"🖼️ {uye.name}",
        color=discord.Color.blurple()
    )

    embed.set_image(
        url=uye.display_avatar.url
    )

    await interaction.response.send_message(
        embed=embed
    )


# =========================================================
# /İSTATİSTİK
# =========================================================

@bot.tree.command(
    name="istatistik",
    description="ZET istatistiklerini gösterir."
)
async def istatistik(interaction):

    toplam_uye = sum(
        guild.member_count or 0
        for guild in bot.guilds
    )

    embed = discord.Embed(
        title="📊 ZET İstatistikleri",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="🌐 Sunucu",
        value=str(len(bot.guilds)),
        inline=True
    )

    embed.add_field(
        name="👥 Üye",
        value=str(toplam_uye),
        inline=True
    )

    embed.add_field(
        name="⚡ Komut",
        value=str(
            len(bot.tree.get_commands())
        ),
        inline=True
    )

    await interaction.response.send_message(
        embed=embed
    )


# =========================================================
# /BAN
# =========================================================

@bot.tree.command(
    name="ban",
    description="Bir kullanıcıyı sunucudan yasaklar."
)
@discord.app_commands.checks.has_permissions(
    ban_members=True
)
async def ban(
    interaction,
    uye: discord.Member,
    sebep: str = "Belirtilmedi"
):

    await uye.ban(
        reason=sebep
    )

    await interaction.response.send_message(
        f"🔨 **{uye}** sunucudan yasaklandı.\n"
        f"Sebep: {sebep}"
    )


# =========================================================
# /KICK
# =========================================================

@bot.tree.command(
    name="kick",
    description="Bir kullanıcıyı sunucudan atar."
)
@discord.app_commands.checks.has_permissions(
    kick_members=True
)
async def kick(
    interaction,
    uye: discord.Member,
    sebep: str = "Belirtilmedi"
):

    await uye.kick(
        reason=sebep
    )

    await interaction.response.send_message(
        f"👢 **{uye}** sunucudan atıldı.\n"
        f"Sebep: {sebep}"
    )


# =========================================================
# /TIMEOUT
# =========================================================

@bot.tree.command(
    name="timeout",
    description="Bir kullanıcıya zaman aşımı verir."
)
@discord.app_commands.checks.has_permissions(
    moderate_members=True
)
async def timeout(
    interaction,
    uye: discord.Member,
    dakika: int,
    sebep: str = "Belirtilmedi"
):

    if dakika < 1:

        await interaction.response.send_message(
            "❌ Süre en az 1 dakika olmalıdır."
        )

        return

    await uye.timeout(
        timedelta(minutes=dakika),
        reason=sebep
    )

    await interaction.response.send_message(
        f"⏱️ **{uye}** {dakika} dakika "
        f"timeout aldı."
    )


# =========================================================
# /TEMİZLE
# =========================================================

@bot.tree.command(
    name="temizle",
    description="Kanaldaki mesajları temizler."
)
@discord.app_commands.checks.has_permissions(
    manage_messages=True
)
async def temizle(
    interaction,
    miktar: int
):

    if miktar < 1 or miktar > 100:

        await interaction.response.send_message(
            "❌ 1 ile 100 arasında bir sayı gir."
        )

        return

    await interaction.response.defer(
        ephemeral=True
    )

    silinen = await interaction.channel.purge(
        limit=miktar
    )

    await interaction.followup.send(
        f"🧹 {len(silinen)} mesaj temizlendi."
    )


# =========================================================
# KARŞILAMA
# =========================================================

@bot.event
async def on_member_join(member):

    if not ayarlar["karsilama"]:
        return

    kanal = discord.utils.get(
        member.guild.text_channels,
        name="hos-geldin"
    )

    if kanal is None:
        return

    mesaj = mesajlar["karsilama"]

    mesaj = mesaj.replace(
        "{uye}",
        member.mention
    )

    mesaj = mesaj.replace(
        "{uyesayisi}",
        str(member.guild.member_count)
    )

    await kanal.send(mesaj)


# =========================================================
# AYRILMA
# =========================================================

@bot.event
async def on_member_remove(member):

    if not ayarlar["ayrilma"]:
        return

    kanal = discord.utils.get(
        member.guild.text_channels,
        name="hosca-kal"
    )

    if kanal is None:
        return

    mesaj = mesajlar["ayrilma"]

    mesaj = mesaj.replace(
        "{uye}",
        str(member)
    )

    mesaj = mesaj.replace(
        "{uyesayisi}",
        str(member.guild.member_count)
    )

    await kanal.send(mesaj)


# =========================================================
# PANELİ BAŞLAT
# =========================================================

def panel_baslat():

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv("PORT", "5000")
        ),
        debug=False,
        use_reloader=False
    )


threading.Thread(
    target=panel_baslat,
    daemon=True
).start()


# =========================================================
# BOTU BAŞLAT
# =========================================================

token = os.getenv("ZET_TOKEN")

if not token:

    print("❌ ZET_TOKEN bulunamadı!")

else:

    bot.run(token)