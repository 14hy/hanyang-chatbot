"""examples 안에 있는 .rive 파일들을 테스트 합니다."""

from rivescript import RiveScript

bot = RiveScript(utf8=True)
bot.load_directory("./examples")
bot.sort_replies()

while True:
    msg = input('You> ')
    if msg == '/quit':
        quit()

    reply = bot.reply("localuser", msg)
    print(f'Bot > {reply}')
