from aiogram import *
import requests
from bs4 import *
from aiogram.types import *

bot = Bot(token="6250006296:AAEC4Lnx2z2pNBKY0XBYVIbWP-WMohoEr_w")

dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, f"Hello {message.from_user.full_name}. Welcome to our bot.")
    await bot.send_message(message.chat.id, "What are you looking for?")

@dp.message_handler(content_types=["text"])
async def parse_info(message: types.Message):
    await bot.send_message(message.chat.id, "Please wait...")
    text = message.text.replace(" ", "+")
    res = requests.get(f"https://github.com/search?q={text}").text
    soup = BeautifulSoup(res, "html.parser")
    repo_list = soup.select(".repo-list-item.hx_hit-repo.d-flex.flex-justify-start.py-4.public.source")

    if not repo_list:
        users = requests.get(f"https://github.com/search?q={text}&type=users").text
        users_list = BeautifulSoup(users, "html.parser")

        user_names = [user.find_all_next("a", class_="color-fg-muted") for user in users_list]

        links = []

        if user_names:
            for user in user_names:
                try:
                    links.append(user[0]['href'])
                except IndexError:
                    pass
            for i in set(links):
                await bot.send_message(message.chat.id, 'https://github.com/' + i)

        else:
            await bot.send_message(message.chat.id, "Nothing found!")

    else:
        for repo in repo_list:
            repo_name = repo.select_one(".mt-n1.flex-auto").select_one("div", class_="d-flex").select_one("div", class_=".f4.text-normal").select_one("a", class_=".v-align-middle")
            href = f"""https://github.com/{repo_name["href"]}"""
            
            if requests.get(href + "/archive/refs/heads/main.zip").status_code == 200:
                yuk = InlineKeyboardMarkup(row_width=1)
                la = InlineKeyboardButton("Download code", callback_data="la", url=f"{href}/archive/refs/heads/main.zip")
                yuk.add(la)
                await bot.send_message(message.chat.id, href, reply_markup=yuk)
            else:
                yuk = InlineKeyboardMarkup(row_width=1)
                la = InlineKeyboardButton("Download code", callback_data="la", url=f"{href}/archive/refs/heads/master.zip")
                yuk.add(la)
                await bot.send_message(message.chat.id, href, reply_markup=yuk)
        
@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await bot.send_message(message.chat.id, "Contact @Nodir_Bahodirov!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
