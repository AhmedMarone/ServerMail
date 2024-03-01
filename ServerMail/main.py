import discord
from discord.ext import commands
from discord import app_commands
from discord import Button
from discord import ButtonStyle
from discord import components
from discord import Button, ButtonStyle
from discord import ActionRow
from discord.ext.commands import has_permissions, check


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@bot.event
async def on_ready():
    print("Bot running with")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)
    await bot.change_presence(activity=discord.Game(name="/about"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name='servermail', description="📬 Envoyer un message privé personnalisé avec un embed de serveur")
async def servermp_command(
    interaction, 
    user: discord.User, 
    mail: str
):
    member = interaction.user

    if not (member.guild_permissions.administrator or member.id == interaction.guild.owner_id):
        embed = discord.Embed(description="🔒 **Vous n'avez pas les autorisations nécessaires pour exécuter cette commande.**", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # Vérifier si l'utilisateur existe dans le serveur
    target_member = interaction.guild.get_member(user.id)
    if target_member is None:
        embed = discord.Embed(description="❌ **Cet utilisateur n'est pas dans ce serveur.**", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    try:
        servermp_embed = discord.Embed(description=mail, color=discord.Color(int("0x7289DA", 16)))
        
        # Placer le profil du serveur à gauche de l'embed
        servermp_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        servermp_embed.set_thumbnail(url=interaction.guild.icon)  # Ajout de l'image du serveur dans le carré

        # Envoyer le message au membre visé
        await target_member.send(embed=servermp_embed)

        embed_success = discord.Embed(description="✉️ *Message envoyé avec succès.*", color=discord.Color.green())
        await interaction.response.send_message(embed=embed_success, ephemeral=True)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message privé : {e}")
        embed = discord.Embed(description="**❌  Erreur lors de l'envoi du message privé.**", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)



# Lancer le bot
bot.run("Token here")