
                                                    #default settings

import discord
from discord.ext import commands
from distro import name
from bots.ds_bot.dayvinshik.databace import init_db, save_user_profile, get_user_profile, search_profiles
import random
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
discord_token = "API_KEY"
user_data = []
your_way = "YOUR WAY TO FILES"

                                                    # default command
@bot.event
async def on_ready():
    init_db()
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")
    
    
@bot.command()
async def ping(ctx):
    await ctx.send(f"привет, {ctx.author.display_name}!")


                                                            #start
@bot.command()
async def start(ctx):
    with open(f"{your_way}\\baner.png", "rb") as f:
        discord_file = discord.File(f, filename="f.png")
        embed = discord.Embed(title="Новая анкета", description="Здравствуй! Хочешь создать анкету?", color=discord.Colour.greyple())
        embed.set_image(url="attachment://f.png")
        view = Button_Menu()
        await ctx.send(file=discord_file, embed=embed, view=view)
        
                                                # send profile for user
@bot.command()
async def profile(ctx):
    profile_data = get_user_profile(ctx.author.id)
    with open(profile_data[3], "rb") as f:
        if profile_data:
            name, age, sex, photo_url, description, follows = profile_data
            discord_file = discord.File(f, filename=f"f.png")
            embed = discord.Embed(title=f"Ваш профиль \n -----------------------", description=f"Имя: {name}\n Возраст: {age}\n Пол: {sex} \n Описание: {description} \n Кого ищу: {follows} \n -----------------------", color=discord.Colour.green())
            embed.set_image(url=f"attachment://f.png")
            await ctx.send(file=discord_file, embed=embed)

                                                                #help
@bot.command()
async def help_user(ctx):
    help_text = """
    **Команды бота:**
    `!ping` - Приветствие
    `!profile` - Просмотреть профиль
    `!start` - Начать создание анкеты
    `!help` - Показать это сообщение
    """
    await ctx.send(help_text)
    
                                                            #MAIN MENU
@bot.command()
async def main(ctx):
    
    with open(f"{your_way}\\baner.png", "rb") as f:
        
        discord_file = discord.File(f, filename="f.png")
        embed = discord.Embed(title="Войди на сервер для роботы бота!", description="Здравствуй! Начнем?", color=discord.Colour.greyple())
        embed.set_image(url="attachment://f.png")
        view = Default_btn_menu(ctx)
        try:
            await ctx.send(file=discord_file, embed=embed, view=view)
        except:
            await ctx.followup.send(file=discord_file, embed=embed, view=view)
        
        
                                                    #SAVE PROFILE BUTTON
                                                    
class save_profile(discord.ui.View):
    
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green, custom_id="yes_button", row=0)
    async def yes_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(user_data)
        await interaction.response.defer()
        save_user_profile(interaction.user.id, user_data[0], int(user_data[1]), user_data[2], user_data[3], user_data[4], user_data[5])
        await interaction.followup.send("Профиль сохранен!", ephemeral=True)
        await main(interaction)
        
    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red, custom_id="no_button", row=0)
    async def no_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Вы нажали кнопку 'Нет'!", ephemeral=True)
        await Button_Menu.yes_button_callback(self, interaction, button)

                                                        #MAIN MENU BUTTON

class Default_btn_menu(discord.ui.View):
    
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(discord.ui.Button(label="**💌наш сервер**", style=discord.ButtonStyle.link, url="https://discord.gg/j66TrknRAU"))
        
    @discord.ui.button(label="**🔍поиск**", style=discord.ButtonStyle.green, custom_id="search_button", row=0)
    async def search_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.ctx.author.id not in [member.id for member in interaction.guild.members]:
            await interaction.response.send_message("Пожалуйста, присоединитесь к серверу, чтобы использовать эту функцию.", ephemeral=True)
            return
        
        else:
            print("Вы нажали кнопку '🔍поиск'!")
            await search_func(self.ctx)
            
    @discord.ui.button(label="**👤анкета**", style=discord.ButtonStyle.red, custom_id="default_no_button", row=0)
    async def default_no_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await profile(self.ctx)
        
    @discord.ui.button(label="**⚙️настраиваемый поиск**", style=discord.ButtonStyle.blurple, custom_id="default_settings_button", row=0)
    async def default_settings_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.ctx.author.id not in [member.id for member in interaction.guild.members]:
            await interaction.response.send_message("Пожалуйста, присоединитесь к серверу, чтобы использовать эту функцию.", ephemeral=True)
            return
        else:
            print("Вы нажали кнопку '⚙️настраиваемый поиск'!")
            await option_func(self.ctx)

        

                                                #BUTTON FOR CREATE PROFILE

class Button_Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Да", style=discord.ButtonStyle.green, custom_id="yes_button", row=0)
    async def yes_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        global user_data
        await interaction.response.send_message("тогда тебе нужно заполнить анкету, фото(по желанию), имя, возраст, пол. (если добавляете картинку то все одним сообщением)", ephemeral=True)
        user_message = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
        print(interaction.user.display_name, "said", user_message.content)
        user_data = list(map(str.strip, user_message.content.split(" ")))
        
        
        if int(user_data[1]) <= 0 or int(user_data[1]) >= 100:
            await interaction.followup.send("Пожалуйста, укажите корректный возраст (от 0 до 100).", ephemeral=True)
            return
        if user_data[2]=="парень" or user_data[2]=="мужчина" or user_data[2]=="м":
            user_data[2] = "м"
        elif user_data[2]=="девушка" or user_data[2]=="женщина" or user_data[2]=="д":
            user_data[2] = "д"
        else:
            await interaction.followup.send("Пожалуйста, укажите пол как 'парень', 'девушка', 'мужчина', 'женщина', 'м' или 'д'. (если вы гендерно нейтральный то укажите это в описании)", ephemeral=True)
            return
        print(user_data)
        try:
            await user_message.attachments[0].save(f"{your_way}\\{interaction.user.id}.png")
            user_data.append(f"{your_way}\\{interaction.user.id}.png")
            
        except IndexError:
            user_data.append(f"{your_way}\\default_avatar.png")
            
        if len(user_data) < 3:
            await interaction.followup.send("Пожалуйста, предоставьте имя, возраст и пол в правильном формате (например: 'Имя Возраст Пол').", ephemeral=True)
            return
        await interaction.followup.send("теперь расскажи о себе:", ephemeral=True)
        description_message = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
        user_data.append(description_message.content)
        await interaction.followup.send("теперь кого ищешь:", ephemeral=True)
        follows = await bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
        user_data.append(follows.content)
        view = save_profile(interaction)
        
        await interaction.followup.send(f"имя: {user_data[0]} \n возраст: {user_data[1]} \n пол: {user_data[2]} \n описание: {user_data[4]} \n кого ищу: {user_data[5]} \n все верно?", ephemeral=True, view=view)
    
    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red, custom_id="no_button", row=0)
    async def no_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        await interaction.response.send_message("Вы нажали кнопку 'Нет'!", ephemeral=True)
        
        
        
                                                #FUNC FOR RANDOM SEARCH
        
async def search_func(ctx):
    users = search_profiles("any", 0, 100, ctx.author.id)
    for i in range(0, len(users)):
        
        random_profile = random.randint(0, len(users) - 1)
        a = get_user_profile(users[random_profile][0])
        id_random_profile = users[random_profile][0]
        users.pop(random_profile)
        
        with open(a[3], "rb") as f:
            
            if a:
                name, age, sex, photo_url, description, follows = a
                discord_file = discord.File(f, filename=f"f.png")
                
                
                view = discord.ui.View()
                view.add_item(discord.ui.Button(label="Лайк", style=discord.ButtonStyle.green, custom_id="like_button", row=0))
                view.add_item(discord.ui.Button(label="Дизлайк", style=discord.ButtonStyle.red, custom_id="dislike_button", row=0))
                
                
                embed = discord.Embed(title=f"**-----------------------**", description=f"Имя: **{name}**\n Возраст: **{age}**\n Пол: **{sex}** \n Описание: **{description}** \n Кого ищет: **{follows}** \n **-----------------------**", color=discord.Colour.green())
                embed.set_image(url=f"attachment://f.png")
                await ctx.send(file=discord_file, embed=embed, view=view)
                user_answ = await bot.wait_for("interaction", check=lambda i: i.data.get("custom_id") in ["like_button", "dislike_button"] and i.user == ctx.author)
                ctx.defer()
                
                if user_answ.data.get("custom_id") == "like_button":
                    await ctx.send("Вы лайкнули этот профиль!")
                    await like_func(ctx, id_random_profile)
                    
                elif user_answ.data.get("custom_id") == "dislike_button":
                    await ctx.send("Вы дизлайкнули этот профиль!")
                    
                else:
                    await ctx.send("Пожалуйста, ответьте 'лайк' или 'дизлайк'.")
                    return
                
    await ctx.send("к сожелению, пользователи подходящие вам закончились, или не были найдены!")



                                    #FUNC FOR SEARCH WITH OPTIONS
async def option_func(ctx):
    
    options = []
    view = discord.ui.View()
    
    button1 = discord.ui.Button(label="Парень", style=discord.ButtonStyle.grey, custom_id="man_button", row=0)
    button2 = discord.ui.Button(label="Девушка", style=discord.ButtonStyle.grey, custom_id="woman_button", row=0)
    button3 = discord.ui.Button(label="Любой", style=discord.ButtonStyle.grey, custom_id="any_button", row=0)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    
    await ctx.send("Кого ты ищешь?", view=view)
    answr = await bot.wait_for("interaction", check=lambda i: i.data.get("custom_id") in ["man_button", "woman_button", "any_button"] and i.user == ctx.author)
    
    await answr.response.defer()
    if answr.data.get("custom_id") == "man_button":
        await ctx.send("Ты выбрал: Парень")
        options.append("м")
        await ctx.defer()
    elif answr.data.get("custom_id") == "woman_button":
        await ctx.send("Ты выбрал: Девушка")
        options.append("д")
        await ctx.defer()
    elif answr.data.get("custom_id") == "any_button":
        await ctx.send("Ты выбрал: Любой")
        options.append("any")
        await ctx.defer()
    view.clear_items()
    view.add_item(discord.ui.Button(label="**12-16**", style=discord.ButtonStyle.green, custom_id="young_button", row=0))
    view.add_item(discord.ui.Button(label="**17-20**", style=discord.ButtonStyle.green, custom_id="teenager_button", row=0))
    view.add_item(discord.ui.Button(label="**21+**", style=discord.ButtonStyle.green, custom_id="adult_button", row=0))
    
    await ctx.send("Выбери возрастной диапазон:", view=view)
    answr = await bot.wait_for("interaction", check=lambda i: i.data.get("custom_id") in ["young_button", "teenager_button", "adult_button"] and i.user == ctx.author)
    
    await answr.response.defer()
    if answr.data.get("custom_id") == "young_button":
        await ctx.send("Ты выбрал: 12-16")
        options.append(12)
        options.append(16)
        await ctx.defer()
    elif answr.data.get("custom_id") == "teenager_button":
        await ctx.send("Ты выбрал: 17-20")
        options.append(17)
        options.append(20)
        await ctx.defer()
    elif answr.data.get("custom_id") == "adult_button":
        await ctx.send("Ты выбрал: 21+")
        options.append(21)
        options.append(100)
        await ctx.defer()
        
    print(options)
    search_results = search_profiles(options[0], options[1], options[2], ctx.author.id)
    print(search_results)
    
    await ctx.send(f"Найдено {len(search_results)} профилей, соответствующих вашим критериям.")
    
    for i in range(0, len(search_results)):
        
        random_profile = random.randint(0, len(search_results) - 1)
        a = get_user_profile(search_results[random_profile][0])
        id_random_profile = search_results[random_profile][0]
        search_results.pop(random_profile)
        
        with open(a[3], "rb") as f:
            
            if a:
                
                name, age, sex, photo_url, description, follows = a
                discord_file = discord.File(f, filename=f"f.png")
                
                
                view = discord.ui.View()
                view.add_item(discord.ui.Button(label="Лайк", style=discord.ButtonStyle.green, custom_id="like_button", row=0))
                view.add_item(discord.ui.Button(label="Дизлайк", style=discord.ButtonStyle.red, custom_id="dislike_button", row=0))
                
                
                embed = discord.Embed(title=f"**-----------------------**", description=f"Имя: **{name}**\n Возраст: **{age}**\n Пол: **{sex}** \n Описание: **{description}** \n Кого ищет: **{follows}** \n **-----------------------**", color=discord.Colour.green())
                embed.set_image(url=f"attachment://f.png")
                await ctx.send(file=discord_file, embed=embed, view=view)
                user_answ = await bot.wait_for("interaction", check=lambda i: i.data.get("custom_id") in ["like_button", "dislike_button"] and i.user == ctx.author)
                ctx.defer()
                
                if user_answ.data.get("custom_id") == "like_button":
                    await ctx.send("Вы лайкнули этот профиль!")
                    await like_func(ctx, id_random_profile)
                    
                elif user_answ.data.get("custom_id") == "dislike_button":
                    await ctx.send("Вы дизлайкнули этот профиль!")
                    
                else:
                    await ctx.send("Пожалуйста, ответьте 'лайк' или 'дизлайк'.")
                    return
                
    await ctx.send("к сожелению, пользователи подходящие вам закончились, или не были найдены!")
    
                                                #FUNC FOR LIKE OTHER PROFILE

async def like_func(ctx, profile_id):
    target_user = bot.get_user(profile_id) or await bot.fetch_user(profile_id)
    main_user = get_user_profile(ctx.author.id)
    with open(main_user[3], "rb") as f:
        if main_user:
            name, age, sex, photo_url, description, follows = main_user
            discord_file = discord.File(f, filename=f"f.png")
            
            view = discord.ui.View()
            view.add_item(discord.ui.Button(label="💌профиль", style=discord.ButtonStyle.green, url=f"https://discord.com/users/{ctx.author.id}"))
            view.add_item(discord.ui.Button(label="🔍поиск", style=discord.ButtonStyle.green, custom_id="search_button", row=0))
            
            embed = discord.Embed(title=f"**Вас лайнул <{ctx.author.name}>** \n -----------------------", description=f"Имя: {name}\n Возраст: {age}\n Пол: {sex} \n Описание: {description} \n Кого ищу: {follows} \n -----------------------", color=discord.Colour.green())
            embed.set_image(url=f"attachment://f.png")
            
            await target_user.send(f"Профилл {ctx.author.name}: <@{ctx.author.id}>", file=discord_file, embed=embed, view=view)
            interaction = await bot.wait_for("interaction", check=lambda i: i.data.get("custom_id") == "search_button" and i.user == target_user)
            
            await interaction.response.defer()
            await search_func(interaction)

bot.run(discord_token)