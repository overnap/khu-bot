# Let us process asynchronously
import asyncio
# Import discord API
import discord
from discord.ext.commands import Bot
# For convenient time handling
from datetime import datetime
from pytz import timezone
# For serializing config
import json
# Import custom crawling module
import crawl

with open("config.json") as file:
    config = json.load(file)

is_running = False
bot = Bot(command_prefix=config["PREFIX"])

channels = []
khuu_data = []
j_data = []
j_meal = []
swb_data = []
swc_data = []
check_meal = [False, False, False]

async def khu_undergraduate_alert():
    crawled = await crawl.khu_undergraduate_crawl()
    for post in crawled:
        exist = any(x == post for x in khuu_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xEB422E)
            embed.set_author(name="KHU 학사", url="https://www.khu.ac.kr/kor/notice/list.do?page=1&category=UNDERGRADUATE", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
            for channel in channels:
                await channel.send(embed=embed)
            khuu_data.append(post)
            # Delete old posts for memory management
            if len(swb_data) > 20:
                khuu_data.pop(0)

async def sw_business_alert():
    crawled = await crawl.sw_business_crawl()
    for post in crawled:
        exist = any(x == post for x in swb_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xE060A4)
            embed.set_author(name="SW 사업단", url="http://swedu.khu.ac.kr/html_2018/", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
            for channel in channels:
                await channel.send(embed=embed)
            swb_data.append(post)
            # Delete old posts for memory management
            if len(swb_data) > 20:
                swb_data.pop(0)

async def sw_college_alert():
    crawled = await crawl.sw_college_crawl()
    for post in crawled:
        exist = any(x == post for x in swc_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xF5D356)
            embed.set_author(name="SW융합대학", url="http://software.khu.ac.kr/html_2018/", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
            for channel in channels:
                await channel.send(embed=embed)
            swc_data.append(post)
            # Delete old posts for memory management
            if len(swb_data) > 20:
                swc_data.pop(0)

async def j_dormitory_alert():
    crawled = await crawl.j_dormitory_crawl()
    for post in crawled:
        exist = any(x == post for x in j_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0x568DF5)
            embed.set_author(name="제2기숙사", url="https://dorm2.khu.ac.kr/dorm2/", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
            for channel in channels:
                await channel.send(embed=embed)
            j_data.append(post)
            # Delete old posts for memory management
            if len(swb_data) > 15:
                j_data.pop(0)

async def j_meal_alert(t:datetime):
    # TODO: It would be good to manage diet data for each channel
    # TODO: Prettify spaghetti code
    global j_meal
    global check_meal
    # Try crawling if it is a new day or do not have data
    if (t.hour > 4 and t.hour < 6 and check_meal.count(True) == 3) or len(j_meal) == 0:
        check_meal = [False, False, False]
        try:
            j_meal = await crawl.j_meal_crawl()
            print("[Main] Got meal data")
        except:
            j_meal = []
            print("[ERROR] Cannot get meal data")
        print("[Main] Today's date :", t.date(), ", day of week :", t.weekday())
    # Check all if meal time have passed or do not have data
    if t.hour > 6 and len(j_meal) == 0:
        print("[Main] No meal data for today!")
        check_meal = [True, True, True]
    elif t.hour > 19:
        check_meal = [True, True, True]
    # Dinner
    elif ((t.hour == 17 and t.minute > 5) or t.hour > 17) and check_meal[2] == False:
        check_meal = [True, True, True]
        embed = discord.Embed(title="제2기숙사", description="석식 메뉴", color=0x59DE6D)
        embed.set_author(name="오늘의 학식", url="https://dorm2.khu.ac.kr/dorm2/40/4050.kmc", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
        if t.weekday() == 5 or t.weekday() == 6:
            # Korean food only on weekends
            embed.add_field(name="한식", value="없음" if j_meal[2] == '' else j_meal[2], inline=False)
        else:
            embed.add_field(name="한식", value="없음" if j_meal[5] == '' else j_meal[5], inline=False)
            embed.add_field(name="일품", value="없음" if j_meal[6] == '' else j_meal[6], inline=False)
        for channel in channels:
            await channel.send(embed=embed)
    # Lunch
    elif ((t.hour == 10 and t.minute > 40) or t.hour > 10) and check_meal[1] == False:
        check_meal = [True, True, False]
        embed = discord.Embed(title="제2기숙사", description="중식 메뉴", color=0x59DE6D)
        embed.set_author(name="오늘의 학식", url="https://dorm2.khu.ac.kr/dorm2/40/4050.kmc", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
        if t.weekday() == 5 or t.weekday() == 6:
            # Korean food only on weekends
            embed.add_field(name="한식", value="없음" if j_meal[1] == '' else j_meal[1], inline=False)
        else:
            # Lunch has first class 1 and first class 2
            embed.add_field(name="한식", value="없음" if j_meal[2] == '' else j_meal[2], inline=False)
            embed.add_field(name="일품1", value="없음" if j_meal[3] == '' else j_meal[3], inline=False)
            embed.add_field(name="일품2", value="없음" if j_meal[4] == '' else j_meal[4], inline=False)
        for channel in channels:
            await channel.send(embed=embed)
    # Breakfast
    elif ((t.hour == 7 and t.minute > 40) or t.hour > 7) and check_meal[0] == False:
        check_meal = [True, False, False]
        embed = discord.Embed(title="제2기숙사", description="조식 메뉴", color=0x59DE6D)
        embed.set_author(name="오늘의 학식", url="https://dorm2.khu.ac.kr/dorm2/40/4050.kmc", icon_url="http://www.google.com/s2/favicons?domain=https://www.khu.ac.kr/kor/main/index.do")
        if t.weekday() == 5 or t.weekday() == 6:
            # Korean food only on weekends
            embed.add_field(name="한식", value="없음" if j_meal[0] == '' else j_meal[0], inline=False)
        else:
            embed.add_field(name="한식", value="없음" if j_meal[0] == '' else j_meal[0], inline=False)
            embed.add_field(name="일품", value="없음" if j_meal[1] == '' else j_meal[1], inline=False)
        for channel in channels:
            await channel.send(embed=embed)
            
async def main_coroutine():
    # System main coroutine
    
    # To prevent multiple execution
    global is_running
    is_running = True

    # Crawl and alarm
    while True:
        t = datetime.now(timezone("Asia/Seoul"))
        # Record start time
        print("[Main] Coroutine started : " + t.strftime("%Y/%m/%d %H:%M:%S"))

        # For debugging, only work with more than one user
        if len(channels) != 0:
            futures = []
            futures.append(asyncio.ensure_future(khu_undergraduate_alert()))
            futures.append(asyncio.ensure_future(j_dormitory_alert()))
            futures.append(asyncio.ensure_future(j_meal_alert(t)))
            futures.append(asyncio.ensure_future(sw_college_alert()))
            futures.append(asyncio.ensure_future(sw_business_alert()))
            await asyncio.gather(*futures)

        # Record completion time
        print("[Main] Coroutine completed : " + datetime.now(timezone("Asia/Seoul")).strftime("%Y/%m/%d %H:%M:%S"))
        # Repeat with delay
        await asyncio.sleep(config["DELAY"])

@bot.event
async def on_ready():
    print("[BOT] The bot is ready!")

    # Run only once
    global is_running
    if is_running == False:
        await main_coroutine()

@bot.command()
async def start(ctx):
    if channels.count(ctx.channel) == 0:
        channels.append(ctx.channel)
        print("[BOT] The alert started :", ctx.channel)
        await ctx.send("알리미가 시작되었습니다.")
    else:
        await ctx.send("이미 알리미가 실행 중입니다.")

@bot.command()
async def stop(ctx):
    if channels.count(ctx.channel) != 0:
        channels.remove(ctx.channel)
        print("[BOT] The alert stopped :", ctx.channel)
        await ctx.send("알리미가 정지되었습니다.")
    else:
        await ctx.send("알리미가 실행 중이지 않습니다.")

bot.run(config["TOKEN"])