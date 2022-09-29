from ChatBot.ai import ChatAI
from ChatBot.args import get_arguments

def ConsoleBot():
    arguments = get_arguments()
    if arguments.bots == 2:
        bot = ChatAI()
        print('Logged on as the bot!')
        print("Please provide the starting message:")
        sequel_bot_res = input("> ")+"\n"
        orig_bot_res = ""
        
        while True:
            orig_bot_res = bot.generate_response(sequel_bot_res, arguments)
            print("THE ORGINAL: "+orig_bot_res+"\n")
            sequel_bot_res = bot.generate_response(orig_bot_res, arguments)
            print("ELECTRIC BOOGALOO: "+sequel_bot_res+"\n")

    bot = ChatAI()
    print('Logged on as the bot!')

    while True:
        message = input("> ")+"\n"
        if not message.strip() == "":
            res = bot.generate_response(message, arguments)
            print("Chatbot AI: "+res)
            
ConsoleBot()