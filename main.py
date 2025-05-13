import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class OrderModal(discord.ui.Modal, title="Plaats een bestelling"):

    product = discord.ui.TextInput(label="Productnaam", placeholder="Bijv. T-shirt", required=True)
    aantal = discord.ui.TextInput(label="Aantal", placeholder="Bijv. 3", required=True)
    adres = discord.ui.TextInput(label="Adres", style=discord.TextStyle.paragraph, placeholder="Straat, Stad, Postcode", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Nieuwe Bestelling",
            color=discord.Color.green()
        )
        embed.add_field(name="Product", value=self.product.value, inline=False)
        embed.add_field(name="Aantal", value=self.aantal.value, inline=False)
        embed.add_field(name="Adres", value=self.adres.value, inline=False)
        embed.set_footer(text=f"Bestelling geplaatst door {interaction.user}")

        # Stuur embed naar het huidige kanaal
        await interaction.response.send_message(embed=embed)

        # Zoek het 'order logs' kanaal en stuur daar ook de embed
        log_channel = discord.utils.get(interaction.guild.text_channels, name="order-logs")
        if log_channel:
            await log_channel.send(embed=embed)
        else:
            print("Kanaal 'order-logs' niet gevonden.")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online als {bot.user}")

@bot.tree.command(name="order", description="Plaats een bestelling")
async def order(interaction: discord.Interaction):
    await interaction.response.send_modal(OrderModal())

keep_alive()
bot.run("YOUR_BOT_TOKEN")
