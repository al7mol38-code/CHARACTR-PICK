import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# حالة الفارم العامة
farm_status = {
    "is_open": True,
    "setup_message": None  
}

# هيكل تخزين بيانات الفريقين
teams_data = {
    "team_1": {"tank": [], "dps": [], "support": []},
    "team_2": {"tank": [], "dps": [], "support": []}
}

# أيدي الرتب المسموح لها بالإدارة
ALLOWED_ROLE_IDS = [
    1533463601908809748, 1533463600381956118, 1534471459739668570, 
    1533463598129479690, 1533463596812599489, 1533463595831001339, 
    1541351616907583560, 1533463592265977886, 1533463570564649121, 
    1533463569683845160
]

# قائمة التانك
TANK_CHARS = [
    "انجيلا", "هالك", "كابتن أمريكا", "ديدبول", "ديفل داينو", 
    "دكتور سترينج", "إيما فروست", "قروت", "ماقينتو", "بيني باركر", 
    "روق", "ذا هود", "ذا ثينق", "ثور", "فينوم"
]

# قسم الـ DPS الأول
DPS_CHARS_1 = [
    "بلاك كات", "بلاك بانثر", "بلاك ويدو", "بليد", "سايكلوبس", 
    "ديرديفيل", "ديدبول", "اليسا بلودستون", "قور", "هوكاي", 
    "هيلا", "هيومن تورش", "ايرون فيست", "ايرون مان"
]

# قسم الـ DPS الثاني
DPS_CHARS_2 = [
    "ماجيك", "مستر فانتاستيك", "مون نايت", "نامور", "فينيكس", 
    "سايلوك", "سكارليت ويتش", "سبايدر مان", "سكويرل قيرل", 
    "ستار لورد", "ستورم", "بونشر", "وينتر سولجر", "ولفرين"
]

# قائمة السبورت / الهيلر المحدثة
SUPPORT_CHARS = [
    "آدم", "كلوك اند داقر", "ديدبول", "قامبت", "انفزبل ومن", 
    "جيف", "جوبلي", "لوكي", "لونا", "مانتس", 
    "روكيت راكون", "اولترون", "وايت فوكس"
]

def update_main_embed(admin_name):
    embed = discord.Embed(
        title="🎮 فارم 2-2-2",
        description="2 هيلر - 2 دي بي إس - 2 تانك لكل فريق (فريقين)\n\nاختر فريقك ثم رولك ثم شخصيتك",
        color=discord.Color.gold()
    )
    embed.add_field(name="المشرف المسؤول", value=f"⭐ {admin_name}", inline=False)
    status_str = "🔒 مفتوح" if farm_status["is_open"] else "🔒 مغلق"
    embed.add_field(name="حالة الروم", value=status_str, inline=False)

    # الفريق الأول
    t1 = teams_data["team_1"]
    t1_tank_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t1["tank"]]) if t1["tank"] else "لا يوجد"
    t1_dps_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t1["dps"]]) if t1["dps"] else "لا يوجد"
    t1_sup_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t1["support"]]) if t1["support"] else "لا يوجد"

    embed.add_field(name="🔴 الفريق الأول", value=f"🛡️ تانك ({len(t1['tank'])}/2)\n{t1_tank_str}\n⚔️ دي بي إس ({len(t1['dps'])}/2)\n{t1_dps_str}\n💉 هيلر ({len(t1['support'])}/2)\n{t1_sup_str}", inline=False)

    # الفريق الثاني
    t2 = teams_data["team_2"]
    t2_tank_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t2["tank"]]) if t2["tank"] else "لا يوجد"
    t2_dps_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t2["dps"]]) if t2["dps"] else "لا يوجد"
    t2_sup_str = "\n".join([f"{item['user'].mention} - {item['char']}" for item in t2["support"]]) if t2["support"] else "لا يوجد"

    embed.add_field(name="🔵 الفريق الثاني", value=f"🛡️ تانك ({len(t2['tank'])}/2)\n{t2_tank_str}\n⚔️ دي بي إس ({len(t2['dps'])}/2)\n{t2_dps_str}\n💉 هيلر ({len(t2['support'])}/2)\n{t2_sup_str}", inline=False)

    return embed

def has_admin_role(member):
    if not isinstance(member, discord.Member):
        return False
    if member.guild_permissions.administrator:
        return True
    return any(role.id in ALLOWED_ROLE_IDS for role in member.roles)

class CharacterSelect(discord.ui.Select):
    def __init__(self, char_list, team_key, role_key, admin_name):
        self.char_list = char_list
        self.team_key = team_key
        self.role_key = role_key
        self.admin_name = admin_name
        options = [discord.SelectOption(label=name[:100]) for name in char_list]
        super().__init__(placeholder="اختر شخصيتك...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_char = self.values[0]
        user = interaction.user

        for r_key in ["tank", "dps", "support"]:
            teams_data[self.team_key][r_key] = [
                item for item in teams_data[self.team_key][r_key] if item["user"].id != user.id
            ]

        teams_data[self.team_key][self.role_key].append({"user": user, "char": selected_char})

        if farm_status["setup_message"]:
            try:
                new_embed = update_main_embed(self.admin_name)
                await farm_status["setup_message"].edit(embed=new_embed)
            except Exception:
                pass

        await interaction.response.send_message(f"✅ تم تسجيلك بنجاح بشخصية: **{selected_char}** (وتم تحديث رولك تلقائياً).", ephemeral=True)

class DPSGroupSelectView(discord.ui.View):
    def __init__(self, team_key, admin_name):
        super().__init__(timeout=180)
        self.team_key = team_key
        self.admin_name = admin_name

    @discord.ui.button(label='قائمة الـ DPS (1)', style=discord.ButtonStyle.danger, emoji='⚔️')
    async def dps_group_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View(timeout=180)
        view.add_item(CharacterSelect(DPS_CHARS_1, self.team_key, "dps", self.admin_name))
        await interaction.response.send_message("اختر من القائمة الأولى:", view=view, ephemeral=True)

    @discord.ui.button(label='قائمة الـ DPS (2)', style=discord.ButtonStyle.danger, emoji='⚔️')
    async def dps_group_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View(timeout=180)
        view.add_item(CharacterSelect(DPS_CHARS_2, self.team_key, "dps", self.admin_name))
        await interaction.response.send_message("اختر من القائمة الثانية:", view=view, ephemeral=True)

class RoleChoiceView(discord.ui.View):
    def __init__(self, team_key, admin_name):
        super().__init__(timeout=180)
        self.team_key = team_key
        self.admin_name = admin_name

    @discord.ui.button(label='تانك', style=discord.ButtonStyle.primary, emoji='🛡️')
    async def tank_choice(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(teams_data[self.team_key]["tank"]) >= 2:
            is_already_tank = any(item["user"].id == interaction.user.id for item in teams_data[self.team_key]["tank"])
            if not is_already_tank:
                await interaction.response.send_message("❌ عذراً، رول التانك مكتمل في هذا الفريق!", ephemeral=True)
                return

        view = discord.ui.View(timeout=180)
        view.add_item(CharacterSelect(TANK_CHARS, self.team_key, "tank", self.admin_name))
        await interaction.response.send_message("اختر شخصية التانك:", view=view, ephemeral=True)

    @discord.ui.button(label='دي بي إس', style=discord.ButtonStyle.danger, emoji='⚔️')
    async def dps_choice(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(teams_data[self.team_key]["dps"]) >= 2:
            is_already_dps = any(item["user"].id == interaction.user.id for item in teams_data[self.team_key]["dps"])
            if not is_already_dps:
                await interaction.response.send_message("❌ عذراً، رول الدي بي إس مكتمل في هذا الفريق!", ephemeral=True)
                return

        await interaction.response.send_message("اختر مجموعة الـ DPS:", view=DPSGroupSelectView(self.team_key, self.admin_name), ephemeral=True)

    @discord.ui.button(label='سبورت / هيلر', style=discord.ButtonStyle.success, emoji='💉')
    async def support_choice(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(teams_data[self.team_key]["support"]) >= 2:
            is_already_sup = any(item["user"].id == interaction.user.id for item in teams_data[self.team_key]["support"])
            if not is_already_sup:
                await interaction.response.send_message("❌ عذراً، رول الهيلر مكتمل في هذا الفريق!", ephemeral=True)
                return

        view = discord.ui.View(timeout=180)
        view.add_item(CharacterSelect(SUPPORT_CHARS, self.team_key, "support", self.admin_name))
        await interaction.response.send_message("اختر شخصية السبورت:", view=view, ephemeral=True)

class GameNameModal(discord.ui.Modal, title='ادخل اسمك'):
    def __init__(self, team_key, admin_name):
        super().__init__()
        self.team_key = team_key
        self.admin_name = admin_name

    game_name = discord.ui.TextInput(
        label='اكتب اسمك في اللعبة',
        placeholder='subaru',
        required=True,
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'تم تسجيل اسمك: **{self.game_name.value}**. الآن اختر رولك:',
            view=RoleChoiceView(self.team_key, self.admin_name),
            ephemeral=True
        )

class FarmView(discord.ui.View):
    def __init__(self, admin_name):
        super().__init__(timeout=None)
        self.admin_name = admin_name

    @discord.ui.button(label='الفريق الأول', style=discord.ButtonStyle.danger, emoji='🔴', custom_id="farm_team_one_btn_v10")
    async def team_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not farm_status["is_open"]:
            await interaction.response.send_message("🔒 عذراً، الفارم مغلق حالياً!", ephemeral=True)
            return
        if not interaction.user.voice:
            await interaction.response.send_message("❌ يجب أن تكون في روم صوتي!", ephemeral=True)
            return
        await interaction.response.send_modal(GameNameModal("team_1", self.admin_name))

    @discord.ui.button(label='الفريق الثاني', style=discord.ButtonStyle.primary, emoji='🔵', custom_id="farm_team_two_btn_v10")
    async def team_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not farm_status["is_open"]:
            await interaction.response.send_message("🔒 عذراً، الفارم مغلق حالياً!", ephemeral=True)
            return
        if not interaction.user.voice:
            await interaction.response.send_message("❌ يجب أن تكون في روم صوتي!", ephemeral=True)
            return
        await interaction.response.send_modal(GameNameModal("team_2", self.admin_name))

    @discord.ui.button(label='إدارة الفارم (قفل/فتح)', style=discord.ButtonStyle.gray, emoji='⚙️', custom_id="farm_admin_control_btn_v10")
    async def admin_control(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_admin_role(interaction.user):
            await interaction.response.send_message("❌ ليس لديك صلاحية!", ephemeral=True)
            return
        
        farm_status["is_open"] = not farm_status["is_open"]
        if farm_status["setup_message"]:
            try:
                await farm_status["setup_message"].edit(embed=update_main_embed(self.admin_name))
            except Exception:
                pass
        await interaction.response.send_message("تم تغيير حالة الفارم بنجاح.", ephemeral=True)

    @discord.ui.button(label='بدء الفارم', style=discord.ButtonStyle.success, emoji='🚀', custom_id="farm_start_action_btn_v10")
    async def start_farm_action(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not has_admin_role(interaction.user):
            await interaction.response.send_message("❌ ليس لديك صلاحية!", ephemeral=True)
            return

        # جمع كل المستخدمين المسجلين في الفريقين (بدون تكرار لو شخص سجل بالغلط)
        all_users = set()
        for team_key in ["team_1", "team_2"]:
            for role_key in ["tank", "dps", "support"]:
                for item in teams_data[team_key][role_key]:
                    all_users.add(item["user"])

        if not all_users:
            await interaction.response.send_message("⚠️ لا يوجد أي لاعب مسجل في الفرق حالياً!", ephemeral=True)
            return

        mentions_str = " ".join([user.mention for user in all_users])
        message_content = (
            f"{mentions_str}\n\n"
            "**بدء الفارم ونتمنى من الجميع الاحترام والالتزام بتعليمات المنظم ونتمنى لكم وقت ممتع**"
        )

        await interaction.channel.send(message_content)
        await interaction.response.send_message("✅ تم إرسال رسالة بدء الفارم ومنشن المسجلين بنجاح.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    view = FarmView("مشرف")
    if not any(isinstance(v, FarmView) for v in bot.persistent_views):
        bot.add_view(view)

is_setting_up = False

@bot.command(name='setup')
async def setup_panel(ctx):
    global is_setting_up
    if is_setting_up:
        return

    if not has_admin_role(ctx.author) and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ لا تمتلك صلاحية استخدام هذا الأمر.")
        return

    is_setting_up = True
    try:
        global teams_data
        teams_data = {
            "team_1": {"tank": [], "dps": [], "support": []},
            "team_2": {"tank": [], "dps": [], "support": []}
        }
        farm_status["is_open"] = True

        if farm_status["setup_message"]:
            try:
                await farm_status["setup_message"].delete()
            except Exception:
                pass

        admin_name = ctx.author.display_name
        embed = update_main_embed(admin_name)
        
        msg = await ctx.send(embed=embed, view=FarmView(admin_name))
        farm_status["setup_message"] = msg
    finally:
        is_setting_up = False

@bot.command(name='كشف')
async def kashf_panel(ctx):
    if not has_admin_role(ctx.author) and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ لا تمتلك صلاحية استخدام هذا الأمر.")
        return

    if farm_status["setup_message"]:
        try:
            await farm_status["setup_message"].delete()
        except Exception:
            pass

    try:
        await ctx.message.delete()
    except Exception:
        pass

    admin_name = ctx.author.display_name
    embed = update_main_embed(admin_name)
    
    msg = await ctx.send(embed=embed, view=FarmView(admin_name))
    farm_status["setup_message"] = msg

@bot.command(name='ازاله')
async def remove_user(ctx, member: discord.Member = None):
    if not has_admin_role(ctx.author) and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ لا تمتلك صلاحية استخدام هذا الأمر.")
        return

    if not member:
        await ctx.send("❌ يرجى الإشارة إلى العضو المراد إزالته، مثال: `!ازاله @اسم_العضو`")
        return

    removed = False
    for team_key in ["team_1", "team_2"]:
        for role_key in ["tank", "dps", "support"]:
            initial_len = len(teams_data[team_key][role_key])
            teams_data[team_key][role_key] = [
                item for item in teams_data[team_key][role_key] if item["user"].id != member.id
            ]
            if len(teams_data[team_key][role_key]) < initial_len:
                removed = True

    if removed:
        if farm_status["setup_message"]:
            try:
                admin_name = ctx.author.display_name
                await farm_status["setup_message"].edit(embed=update_main_embed(admin_name))
            except Exception:
                pass
        await ctx.send(f"✅ تمت إزالة العضو {member.mention} من القائمة بنجاح.")
    else:
        await ctx.send(f"⚠️ العضو {member.mention} غير مسجل في أي فريق أساساً.")

    try:
        await ctx.message.delete()
    except Exception:
        pass

bot.run(TOKEN)
