import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # مهم جداً للتحقق من الروم الصوتي
bot = commands.Bot(command_prefix='!', intents=intents)

# حالة الفارم العامة (مفتوح بشكل افتراضي)
farm_status = {
    "is_open": True
}

# 1. شخصيات التانك (Tanks)
TANK_IMAGES = {
    "كابتن أمريكا (Captain America)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920249812058172/video_60.mp4?ex=6ab0168a&is=6aaec50a&hm=71c7b6d6c2165af7c9c051e746ecbb841abb1a6e7391ef656ea534d49c664573&",
    "بروس بانر / هالك (Bruce Banner / Hulk)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920762125197382/video_48.mp4?ex=6ab01704&is=6aaec584&hm=b6a5b0644821f24d84c2e02fd2cbb0ba443c5b580bb2d0ac3c864c9a0aab919f&",
    "فينوم (Venom)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550921633022222536/video_19.mp4?ex=6ab017d4&is=6aaec654&hm=117b0fb9252dfbe234ab1b7a32efb6a0d68fb61f1b3d191fb4a40b86cf365061&",
    "ثور (Thor)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550921570577285130/video_13.mp4?ex=6ab017c5&is=6aaec645&hm=afd40f7b417004eb16c2caf0f189041aa1307f24084724fb4ea24b783b28eee6&",
    "ماجنيتو (Magneto)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550921819844771911/video_34.mp4?ex=6ab01800&is=6aaec680&hm=49c6560265e7f4d10432bdcd88018c432d1d28185717879a88528ad54c744a24&",
    "دكتور سترينج (Doctor Strange)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920453579743353/video_54.mp4?ex=6ab016ba&is=6aaec53a&hm=8c282138eba5b51f907b4312b437ae77bc621f9b84cbe83b2e525e1bfb4b7e31&",
    "جروت (Groot)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920452879155240/video_53.mp4?ex=6ab016ba&is=6aaec53a&hm=df7cde39ed1dfac92a8a733ce3f24dabb663c452fa550196f8448dea2e288003&",
    "بيني باركر (Peni Parker)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920765015195678/video_30.mp4?ex=6ab01705&is=6aaec585&hm=98af71f38ece63ca076c84b24886d398b73fb6836d20d549f494ada40a486fb3&",
    "الشيء (The Thing)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550921633466683443/video_20.mp4?ex=6ab017d4&is=6aaec654&hm=0d4d987f6d4dc1b55e6924dba477ad029f95a679711ce134d1894a2763049151&",
    "إيما فروست (Emma Frost)": "https://cdn.discordapp.com/attachments/1550919639532306482/1550920506486558750/video_42.mp4?ex=6ab016c7&is=6aaec547&hm=3d29c40623ea080e1c51cc39f8bd5cfd69118a712287f3c9eff61de99284185c&",
    "أنجيلا (Angela)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890826966634537/993BAF10-AEFA-4277-9D1D-4725F41D0F79.gif?ex=6aaffb23&is=6aaea9a3&hm=c65af04f1f6814ef8a7319da0a353bf6d2138f46fca6a6fd88029445575fb55f&"
}

# 2. شخصيات مسبب الضرر (DPS)
DPS_IMAGES = {
    "الرجل العنكبوت (Spider-Man)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890983720230922/4F6FCEB7-ACD6-4D8F-9235-40C4540F6C96.gif?ex=6aaffb48&is=6aaea9c8&hm=efcedcc4d31d9784fc9ec4b378f37881c69a81cc7d0b8c0f4439b17d6cd86a8e&",
    "الرجل الحديدي (Iron Man)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890921971679232/961C23DF-DA88-4586-85F1-26145781AA71.gif?ex=6aaffb39&is=6aaea9b9&hm=f8aac07d12d3fc92e335d995429b52f322b67e056e9e13347ae151e1d80019e2&",
    "ولفيرين (Wolverine)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550891021183750284/6A6377EF-E4F2-4AE2-B234-37E857DC01AF.gif?ex=6aaffb51&is=6aaea9d1&hm=8e74e075e59c82696f12c484907c808035ffbbefd947f998356b8b43572ec194&",
    "جين غراي / فينيكس (Phoenix)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890982575181864/D4CFEDA3-A6B1-40F0-AEC1-CD84D613655D.gif?ex=6aaffb48&is=6aaea9c8&hm=6bd5e12ca692cfe06eb7b71ae1d84aabe3fef04fc7e66f54675b7906718e982e&",
    "ديدبول (Deadpool)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890829974085662/B6124A6B-495E-4305-984E-47FA5B7F467A.gif?ex=6aaffb24&is=6aaea9a4&hm=7df2be718e1ada7695793fcc940d9375d438c0a0cbd98e4b7f3d84d6d4100a97&",
    "غور جزار الآلهة (Gorr The God Butcher)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550924901819621416/IMG_6028.jpg?ex=6ab01adf&is=6aaec95f&hm=8f58972431e40020537d5945e7454364259973bef5c27cbf2cd8f686e15b5338&",
    "سايلوك (Psylocke)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890981530927204/EB0A2341-C253-42AC-B096-FB294E214445.gif?ex=6aaffb48&is=6aaea9c8&hm=52bfd57858dceeb371bbb9ce66c98cabe15007266e241ae4cae00c79b1abb9df&",
    "ماجيك (Magik)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890925386109149/DF1660CB-E8A6-498D-B088-CB72C551CF38.gif?ex=6aaffb3a&is=6aaea9ba&hm=4056a6407f012faadca77183cb727a154d763cdad977c51675a4282abf449162&",
    "هيلا (Hela)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890877541425243/B164DA73-C02F-499D-9EBF-31AE1C5F5C01.gif?ex=6aaffb2f&is=6aaea9af&hm=aee20e36dafc19a1344f4dc7010780c70408b5df96858c69119c792a2639d290&",
    "الساحرة المستديرة / سكارليت ويتش (Scarlet Witch)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890982977970387/2CF8119E-8CEF-4A9F-AFB0-E244948ADDF5.gif?ex=6aaffb48&is=6aaea9c8&hm=45535a9874af34d27dfbb048033e28a5a9d8e7d984e4341688eaf7b13ee108a7&",
    "المعاقب (The Punisher)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550891017253949550/B2C63E17-D371-43D6-99A2-7A0270911302.gif?ex=6aaffb50&is=6aaea9d0&hm=601304b37a19bbadbcb478d9cadc58cbc6e5a1651d7676ded03a36941e6826dc&",
    "بليد (Blade)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890828472389702/C0999967-3CA3-4FBF-B912-61AE57634DBF.gif?ex=6aaffb23&is=6aaea9a3&hm=adf0871424d1d91a48615321b9c5652c5f753b0eacc78368cb704e419c8991eb&",
    "النمر الأسود (Black Panther)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890827977326623/5657C85D-3C47-42C0-BA6E-8BFA11F53A4E.gif?ex=6aaffb23&is=6aaea9a3&hm=c4b46435a352f6bc252b8de28f5d646b5c09fca546b21093c9d01cb366628626&",
    "الأرملة السوداء (Black Widow)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550925819189133483/IMG_6029.jpg?ex=6ab01bba&is=6aaeca3a&hm=c4f86f80af75a1155def384b6918c5ac6ccc4280585b6cd9c3c25b367a03f46e&",
    "هاوك آي / عين الصقر (Hawkeye)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890874379042826/FDF11A15-F2FD-45CE-82D7-ACAB6DC8E595.gif?ex=6aaffb2e&is=6aaea9ae&hm=bdf8a04f6db763e87bcc0b195f29486b6b8085a5b2d60fbdff74b598ff339c91&",
    "مون نايت (Moon Knight)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890929282617364/8FC39F32-9EB5-4999-A6C2-402E6DBE41B3.gif?ex=6aaffb3b&is=6aaea9bb&hm=9498bb688fb97c1eeebb92e2376a4f76bed0611f6e05f4e44ada1e39e37d9a23&",
    "ستار-لورد (Star-Lord)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550891017803145306/573109C8-A4D0-47E5-ABA5-51FCC0B8F1A7.gif?ex=6aaffb50&is=6aaea9d0&hm=0778932b3692ffce7a324de695abd7ac850f12c99eca5571b56b77bbe3aeb321&",
    "جندي الشتاء / باكي (Winter Soldier)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550891020475179068/5F184C06-BBF2-4C16-9AC9-CF8E9AED87D3.gif?ex=6aaffb51&is=6aaea9d1&hm=f87e3801ea0ff9cc9c6f88526455458b7d05470f570708278909aa52db5465d8&",
    "الشعلة البشرية (Human Torch)": "https://cdn.discordapp.com/attachments/1533463914816471221/1550890878380277901/301659CD-DF46-4D71-BC68-41C204A301A1.gif?ex=6aaffb2f&is=6aaea9af&hm=ecffd3232b9d4b5de8ec434719163b2d623230cae2407bf5c4ce607375401d23&",
    "مستر فانتاستيك (Mister Fantastic)": "
