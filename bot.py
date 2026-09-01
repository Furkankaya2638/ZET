import os
import threading
from datetime import timedelta

import discord
from discord.ext import commands
from flask import Flask, render_template_string, request, redirect


# =========================================================
# ZET - DISCORD
# =========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================================================
# ZET - PANEL
# =========================================================

app = Flask(__name__)

settings = {
    "welcome": True,
    "goodbye": False,
    "register": False,
    "ticket": False,
    "scheduler": False,
    "partner": False,
    "moderation": True,
    "security": True,
    "logs": True,
    "roles": False
}


# =========================================================
# PANEL TASARIMI
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="tr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>ZET</title>

<style>

/* =========================
   TEMEL
========================= */

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100%;
}

body {

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: #ffffff;

    background:

        radial-gradient(
            circle at 10% 10%,
            rgba(124, 58, 237, .55),
            transparent 27%
        ),

        radial-gradient(
            circle at 90% 15%,
            rgba(37, 99, 235, .55),
            transparent 28%
        ),

        radial-gradient(
            circle at 55% 100%,
            rgba(236, 72, 153, .30),
            transparent 32%
        ),

        #070914;

    overflow-x: hidden;
}


/* =========================
   SIDEBAR
========================= */

.sidebar {

    position: fixed;

    left: 0;
    top: 0;

    width: 265px;
    height: 100vh;

    padding: 22px 15px;

    background:
        rgba(7, 10, 25, .97);

    border-right:
        1px solid
        rgba(255,255,255,.08);

    overflow-y: auto;

    z-index: 10;
}


.logo {

    display: flex;

    align-items: center;
    justify-content: center;

    gap: 10px;

    margin-bottom: 25px;

    font-size: 29px;

    font-weight: 900;
}


.logo-icon {

    width: 45px;
    height: 45px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb,
            #ec4899
        );

    box-shadow:
        0 0 25px
        rgba(124,58,237,.55);
}


.logo-text {

    background:
        linear-gradient(
            90deg,
            #a78bfa,
            #60a5fa,
            #f472b6
        );

    -webkit-background-clip: text;

    background-clip: text;

    color: transparent;
}


.server-box {

    padding: 14px;

    margin-bottom: 20px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,.18),
            rgba(37,99,235,.10)
        );

    border:
        1px solid
        rgba(255,255,255,.08);
}


.small {

    font-size: 10px;

    color: #8c96ad;

    letter-spacing: .7px;
}


.category {

    margin:
        20px 8px 8px;

    font-size: 10px;

    font-weight: bold;

    letter-spacing: 1.5px;

    color: #68748f;
}


.menu a {

    display: block;

    padding: 11px 13px;

    margin: 4px 0;

    border-radius: 10px;

    color: #cbd5e1;

    text-decoration: none;

    transition:
        background .2s,
        transform .2s,
        color .2s;
}


.menu a:hover {

    color: white;

    background:
        linear-gradient(
            90deg,
            rgba(109,40,217,.85),
            rgba(37,99,235,.75)
        );

    transform:
        translateX(3px);
}


/* =========================
   ANA ALAN
========================= */

.main {

    margin-left: 265px;

    width:
        calc(100% - 265px);

    min-height: 100vh;

    padding: 32px;

    overflow-x: hidden;
}


.top {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 20px;

    margin-bottom: 26px;
}


h1 {

    margin: 0;

    font-size: 32px;
}


.subtitle {

    margin-top: 7px;

    color: #8f99b1;

    font-size: 14px;
}


.profile {

    padding:
        10px 16px;

    border-radius: 25px;

    background:
        rgba(17,24,39,.78);

    border:
        1px solid
        rgba(255,255,255,.08);

    white-space: nowrap;
}


/* =========================
   İSTATİSTİK KARTLARI
========================= */

.stats-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 18px;

    width: 100%;

    margin-bottom: 28px;
}


.card {

    min-width: 0;

    padding: 22px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15,20,42,.95),
            rgba(9,12,27,.95)
        );

    border:
        1px solid
        rgba(255,255,255,.08);

    box-shadow:
        0 15px 40px
        rgba(0,0,0,.22);
}


.stat-icon {

    width: 45px;
    height: 45px;

    display: flex;

    align-items: center;
    justify-content: center;

    margin-bottom: 13px;

    border-radius: 13px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb,
            #ec4899
        );

    font-size: 21px;
}


.stat-title {

    font-size: 11px;

    color: #8e99b1;

    letter-spacing: .5px;
}


.stat-number {

    margin-top: 5px;

    font-size: 27px;

    font-weight: 800;

    word-break: break-word;
}


/* =========================
   SİSTEMLER
========================= */

.section-title {

    margin:
        0 0 18px;

    font-size: 23px;
}


.system-grid {

    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 18px;

    width: 100%;
}


.system-card {

    min-width: 0;

    padding: 20px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(15,20,42,.96),
            rgba(9,12,27,.96)
        );

    border:
        1px solid
        rgba(255,255,255,.08);

    box-shadow:
        0 15px 40px
        rgba(0,0,0,.20);

    transition:
        transform .2s,
        border-color .2s;
}


.system-card:hover {

    transform:
        translateY(-3px);

    border-color:
        rgba(124,58,237,.45);
}


.system-head {

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 12px;
}


.system-name {

    display: flex;

    align-items: center;

    gap: 10px;

    min-width: 0;

    font-weight: bold;
}


.system-icon {

    width: 40px;
    height: 40px;

    flex-shrink: 0;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 11px;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #ec4899
        );
}


.description {

    min-height: 42px;

    margin:
        14px 0;

    color: #8d97ae;

    font-size: 13px;

    line-height: 1.5;
}


/* =========================
   SWITCH
========================= */

.switch {

    position: relative;

    display: inline-block;

    width: 58px;
    height: 32px;

    flex-shrink: 0;
}


.switch input {

    position: absolute;

    opacity: 0;

    width: 0;
    height: 0;
}


.slider {

    position: absolute;

    left: 0;
    top: 0;
    right: 0;
    bottom: 0;

    width: 58px;
    height: 32px;

    cursor: pointer;

    background: #ef4444;

    border-radius: 999px;

    transition: .25s;

    box-shadow:
        inset 0 0 8px
        rgba(0,0,0,.4);
}


.slider:before {

    content: "";

    position: absolute;

    width: 24px;
    height: 24px;

    left: 4px;
    top: 4px;

    background: #ffffff;

    border-radius: 50%;

    transition: .25s;

    box-shadow:
        0 2px 7px
        rgba(0,0,0,.45);
}


.switch input:checked + .slider {

    background:
        linear-gradient(
            90deg,
            #22c55e,
            #10b981
        );

    box-shadow:
        0 0 15px
        rgba(34,197,94,.32);
}


.switch input:checked + .slider:before {

    transform:
        translateX(26px);
}


/* =========================
   BUTON
========================= */

.button {

    display: inline-block;

    border: 0;

    padding:
        11px 17px;

    border-radius: 10px;

    color: white;

    text-decoration: none;

    font-weight: bold;

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

    cursor: pointer;

    transition:
        transform .2s,
        box-shadow .2s;
}


.button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 9px 25px
        rgba(79,70,229,.35);
}


/* =========================
   AYAR KARTI
========================= */

.settings-card {

    padding: 25px;

    border-radius: 18px;

    background:
        rgba(13,18,37,.95);

    border:
        1px solid
        rgba(255,255,255,.08);
}


.settings-grid {

    display: grid;

    grid-template-columns:
        repeat(2, minmax(0,1fr));

    gap: 20px;
}


.setting-box {

    padding: 20px;

    border-radius: 15px;

    background:
        rgba(6,9,21,.65);

    border:
        1px solid
        rgba(255,255,255,.06);
}


label {

    display: block;

    margin-bottom: 7px;

    color: #aeb8cc;

    font-size: 13px;
}


select,
textarea,
input[type=text] {

    width: 100%;

    padding: 12px;

    margin-bottom: 16px;

    color: white;

    background: #080b16;

    border:
        1px solid
        #30384e;

    border-radius: 9px;

    outline: none;
}


textarea {

    min-height: 135px;

    resize: vertical;
}


/* =========================
   MOBİL / DAR EKRAN
========================= */

@media (max-width: 1150px) {

    .stats-grid {

        grid-template-columns:
            repeat(2, minmax(0,1fr));
    }

    .system-grid {

        grid-template-columns:
            repeat(2, minmax(0,1fr));
    }
}


@media (max-width: 800px) {

    .sidebar {

        width: 210px;
    }

    .main {

        margin-left: 210px;

        width:
            calc(100% - 210px);

        padding: 20px;
    }

    .top {

        align-items: flex-start;

        flex-direction: column;
    }

    .stats-grid,
    .system-grid,
    .settings-grid {

        grid-template-columns: 1fr;
    }
}

</style>

</head>


<body>


<!-- =========================
     SOL MENÜ
========================= -->

<div class="sidebar">

    <div class="logo">

        <div class="logo-icon">
            🤖
        </div>

        <div class="logo-text">
            ZET
        </div>

    </div>


    <div class="server-box">

        <div class="small">
            SUNUCU
        </div>

        <strong>
            ZET Sunucun
        </strong>

    </div>


    <div class="category">
        GENEL
    </div>

    <div class="menu">

        <a href="/">
            🏠 Dashboard
        </a>

        <a href="/ai">
            🤖 ZET AI
        </a>

    </div>


    <div class="category">
        OTOMASYON
    </div>

    <div class="menu">

        <a href="/welcome">
            👋 Karşılama & Ayrılma
        </a>

        <a href="/register">
            📝 Kayıt
        </a>

        <a href="/ticket">
            🎫 Ticket
        </a>

        <a href="/scheduler">
            ⏰ Zamanlayıcı
        </a>

        <a href="/partner">
            📣 Partner / Reklam
        </a>

    </div>


    <div class="category">
        SUNUCU
    </div>

    <div class="menu">

        <a href="/moderation">
            🛡️ Moderasyon
        </a>

        <a href="/security">
            🔐 Güvenlik
        </a>

        <a href="/logs">
            📜 Loglar
        </a>

        <a href="/roles">
            🎭 Roller
        </a>

    </div>


    <div class="category">
        ARAÇLAR
    </div>

    <div class="menu">

        <a href="/stats">
            📊 İstatistik
        </a>

        <a href="/settings">
            ⚙️ Ayarlar
        </a>

    </div>

</div>


<!-- =========================
     ANA PANEL
========================= -->

<div class="main">


{% if page == "home" %}


<div class="top">

    <div>

        <h1>
            Dashboard
        </h1>

        <div class="subtitle">
            ZET sunucu kontrol merkezi
        </div>

    </div>


    <div class="profile">
        🤖 ZET Bot
    </div>

</div>


<div class="stats-grid">


    <div class="card">

        <div class="stat-icon">
            🤖
        </div>

        <div class="stat-title">
            BOT DURUMU
        </div>

        <div class="stat-number">
            ÇEVRİMİÇİ
        </div>

    </div>


    <div class="card">

        <div class="stat-icon">
            👥
        </div>

        <div class="stat-title">
            SUNUCU ÜYELERİ
        </div>

        <div class="stat-number">
            {{ members }}
        </div>

    </div>


    <div class="card">

        <div class="stat-icon">
            ⚡
        </div>

        <div class="stat-title">
            AKTİF SİSTEMLER
        </div>

        <div class="stat-number">
            {{ active }}
        </div>

    </div>


    <div class="card">

        <div class="stat-icon">
            🌐
        </div>

        <div class="stat-title">
            SUNUCULAR
        </div>

        <div class="stat-number">
            {{ guilds }}
        </div>

    </div>


</div>


<h2 class="section-title">
    ⚡ ZET Sistemleri
</h2>


<div class="system-grid">


{% for key, item in features.items() %}


<div class="system-card">


    <div class="system-head">


        <div class="system-name">

            <div class="system-icon">
                {{ item.icon }}
            </div>

            {{ item.name }}

        </div>


        <form
            method="POST"
            action="/toggle/{{ key }}"
        >

            <label class="switch">

                <input
                    type="checkbox"
                    {% if settings[key] %}
                    checked
                    {% endif %}
                    onchange="this.form.submit()"
                >

                <span class="slider"></span>

            </label>

        </form>


    </div>


    <div class="description">
        {{ item.description }}
    </div>


    <a
        class="button"
        href="/{{ key }}"
    >
        Ayarları Aç →
    </a>


</div>


{% endfor %}


</div>


{% elif page == "welcome" %}


<div class="top">

    <div>

        <h1>
            👋 Karşılama & Ayrılma
        </h1>

        <div class="subtitle">
            İki sistemi tek yerden yönet.
        </div>

    </div>

</div>


<div class="settings-grid">


    <div class="settings-card">

        <div class="system-head">

            <div class="system-name">

                <div class="system-icon">
                    👋
                </div>

                Karşılama

            </div>


            <form
                method="POST"
                action="/toggle/welcome"
            >

                <label class="switch">

                    <input
                        type="checkbox"
                        {% if settings["welcome"] %}
                        checked
                        {% endif %}
                        onchange="this.form.submit()"
                    >

                    <span class="slider"></span>

                </label>

            </form>

        </div>


        <div class="setting-box">

            <label>
                Karşılama Kanalı
            </label>

            <select>

                <option>
                    #hos-geldin
                </option>

                <option>
                    #genel
                </option>

                <option>
                    #duyurular
                </option>

            </select>


            <label>
                Karşılama Mesajı
            </label>

            <textarea>🎉 Hoş geldin {user}!

Sunucumuzda artık {members} kişiyiz.

İyi eğlenceler! 🚀</textarea>


            <button
                class="button"
                type="button"
            >
                💾 Kaydet
            </button>

        </div>

    </div>


    <div class="settings-card">

        <div class="system-head">

            <div class="system-name">

                <div class="system-icon">
                    🚪
                </div>

                Ayrılma

            </div>


            <form
                method="POST"
                action="/toggle/goodbye"
            >

                <label class="switch">

                    <input
                        type="checkbox"
                        {% if settings["goodbye"] %}
                        checked
                        {% endif %}
                        onchange="this.form.submit()"
                    >

                    <span class="slider"></span>

                </label>

            </form>

        </div>


        <div class="setting-box">

            <label>
                Ayrılma Kanalı
            </label>

            <select>

                <option>
                    #hosca-kal
                </option>

                <option>
                    #genel
                </option>

                <option>
                    #log
                </option>

            </select>


            <label>
                Ayrılma Mesajı
            </label>

            <textarea>👋 {username} sunucudan ayrıldı.

Sunucumuzda artık {members} kişiyiz.</textarea>


            <button
                class="button"
                type="button"
            >
                💾 Kaydet
            </button>

        </div>

    </div>


</div>


{% else %}


<div class="top">

    <div>

        <h1>
            {{ title }}
        </h1>

        <div class="subtitle">
            ZET sistem ayarları
        </div>

    </div>

</div>


<div class="settings-card">


    <div class="system-head">

        <div class="system-name">

            <div class="system-icon">
                {{ icon }}
            </div>

            {{ title }}

        </div>


        {% if key in settings %}

        <form
            method="POST"
            action="/toggle/{{ key }}"
        >

            <label class="switch">

                <input
                    type="checkbox"
                    {% if settings[key] %}
                    checked
                    {% endif %}
                    onchange="this.form.submit()"
                >

                <span class="slider"></span>

            </label>

        </form>

        {% endif %}

    </div>


    <div class="setting-box">

        <label>
            Kanal
        </label>

        <select>

            <option>
                Kanal seç
            </option>

            <option>
                #genel
            </option>

            <option>
                #duyurular
            </option>

        </select>


        <label>
            Mesaj
        </label>

        <textarea>ZET ayarları burada olacak.</textarea>


        <button
            class="button"
            type="button"
        >
            💾 Kaydet
        </button>

    </div>


</div>


{% endif %}


</div>

</body>

</html>
"""


# =========================================================
# SİSTEMLER
# =========================================================

features = {

    "welcome": {
        "name": "Karşılama & Ayrılma",
        "icon": "👋",
        "description":
            "Yeni gelen ve ayrılan üyeleri yönet."
    },

    "register": {
        "name": "Kayıt",
        "icon": "📝",
        "description":
            "Üyeleri hızlı ve düzenli şekilde kaydet."
    },

    "ticket": {
        "name": "Ticket",
        "icon": "🎫",
        "description":
            "Destek talepleri için ticket sistemi."
    },

    "scheduler": {
        "name": "Zamanlayıcı",
        "icon": "⏰",
        "description":
            "Belirlediğin zamanlarda otomatik mesaj gönder."
    },

    "partner": {
        "name": "Partner / Reklam",
        "icon": "📣",
        "description":
            "Partner ve duyuru sistemlerini yönet."
    },

    "moderation": {
        "name": "Moderasyon",
        "icon": "🛡️",
        "description":
            "Ban, kick, timeout, uyarı ve temizleme."
    },

    "security": {
        "name": "Güvenlik",
        "icon": "🔐",
        "description":
            "Sunucuyu spam ve saldırılara karşı koru."
    },

    "logs": {
        "name": "Loglar",
        "icon": "📜",
        "description":
            "Sunucudaki önemli işlemleri takip et."
    }

}


page_info = {

    "register": ("📝 Kayıt", "📝"),
    "ticket": ("🎫 Ticket", "🎫"),
    "scheduler": ("⏰ Zamanlayıcı", "⏰"),
    "partner": ("📣 Partner / Reklam", "📣"),
    "moderation": ("🛡️ Moderasyon", "🛡️"),
    "security": ("🔐 Güvenlik", "🔐"),
    "logs": ("📜 Loglar", "📜"),
    "roles": ("🎭 Roller", "🎭"),
    "stats": ("📊 İstatistik", "📊"),
    "settings": ("⚙️ Ayarlar", "⚙️"),
    "ai": ("🤖 ZET AI", "🤖")

}


# =========================================================
# DISCORD HAZIR
# =========================================================

@bot.event
async def on_ready():

    try:

        synced = await bot.tree.sync()

        print("")
        print("==============================")
        print("🤖 ZET AKTİF")
        print(f"👤 Bot: {bot.user}")
        print(f"🌐 Sunucu: {len(bot.guilds)}")
        print(f"⚡ Slash komut: {len(synced)}")
        print("==============================")
        print("")

    except Exception as error:

        print("❌ Komut senkronizasyon hatası:")
        print(error)


# =========================================================
# GENEL KOMUTLAR
# =========================================================

@bot.tree.command(
    name="yardim",
    description="ZET komutlarını gösterir"
)
async def yardim(interaction):

    embed = discord.Embed(
        title="🤖 ZET",
        description="ZET komut merkezi",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="ℹ️ Genel",
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


@bot.tree.command(
    name="sunucu",
    description="Sunucu bilgilerini gösterir"
)
async def sunucu(interaction):

    guild = interaction.guild

    if guild is None:

        await interaction.response.send_message(
            "❌ Bu komut sunucuda kullanılmalı."
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


@bot.tree.command(
    name="kullanici",
    description="Kullanıcı bilgilerini gösterir"
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
        name="ID",
        value=str(uye.id),
        inline=False
    )

    embed.add_field(
        name="Hesap oluşturma",
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


@bot.tree.command(
    name="avatar",
    description="Avatar gösterir"
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


@bot.tree.command(
    name="istatistik",
    description="ZET istatistiklerini gösterir"
)
async def istatistik(interaction):

    total_members = sum(
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
        value=str(total_members),
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
# MODERASYON
# =========================================================

@bot.tree.command(
    name="ban",
    description="Kullanıcıyı yasaklar"
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
        f"🔨 **{uye}** yasaklandı.\n"
        f"Sebep: {sebep}"
    )


@bot.tree.command(
    name="kick",
    description="Kullanıcıyı sunucudan atar"
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


@bot.tree.command(
    name="timeout",
    description="Kullanıcıya timeout verir"
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
            "❌ Süre en az 1 dakika olmalı."
        )

        return

    await uye.timeout(
        timedelta(minutes=dakika),
        reason=sebep
    )

    await interaction.response.send_message(
        f"⏳ **{uye}** {dakika} dakika "
        f"timeout aldı."
    )


@bot.tree.command(
    name="temizle",
    description="Mesajları temizler"
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

    deleted = await interaction.channel.purge(
        limit=miktar
    )

    await interaction.followup.send(
        f"🧹 {len(deleted)} mesaj temizlendi."
    )


# =========================================================
# PANEL YARDIMCI
# =========================================================

def panel_data():

    members = sum(
        guild.member_count or 0
        for guild in bot.guilds
    )

    return {
        "settings": settings,
        "features": features,
        "members": members,
        "guilds": len(bot.guilds),
        "active": sum(
            1
            for value in settings.values()
            if value
        )
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def home():

    data = panel_data()

    data["page"] = "home"

    return render_template_string(
        HTML,
        **data
    )


# =========================================================
# AÇ / KAPAT
# =========================================================

@app.route(
    "/toggle/<key>",
    methods=["POST"]
)
def toggle(key):

    if key in settings:

        settings[key] = not settings[key]

    return redirect(
        request.referrer or "/"
    )


# =========================================================
# KARŞILAMA + AYRILMA
# =========================================================

@app.route("/welcome")
def welcome():

    data = panel_data()

    data["page"] = "welcome"

    return render_template_string(
        HTML,
        **data
    )


# =========================================================
# DİĞER SAYFALAR
# =========================================================

@app.route("/<key>")
def other_page(key):

    if key not in page_info:

        return "Sayfa bulunamadı", 404

    title, icon = page_info[key]

    data = panel_data()

    data["page"] = key
    data["key"] = key
    data["title"] = title
    data["icon"] = icon

    return render_template_string(
        HTML,
        **data
    )


# =========================================================
# PANELİ BAŞLAT
# =========================================================

def run_panel():

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


threading.Thread(
    target=run_panel,
    daemon=True
).start()


# =========================================================
# TOKEN
# =========================================================

token = os.getenv("ZET_TOKEN")

if not token:

    print("❌ ZET_TOKEN bulunamadı!")
    print(
        "Discord botunu çalıştırmak için "
        "ZET_TOKEN ayarlanmalı."
    )

else:

    bot.run(token)