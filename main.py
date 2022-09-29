from ChatBot.bot import ChatBot
from ChatBot.args import get_arguments

def main():
    """Main function"""
    args = get_arguments()
    client = ChatBot()
    client.run(args.token)

if __name__ == "__main__":
    main()
