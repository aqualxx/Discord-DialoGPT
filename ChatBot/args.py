import argparse
import sys

def get_arguments():
    parser = argparse.ArgumentParser(description="Discord DialoGPT ChatBot")
    parser.add_argument("--token",              dest="token", help="Input")
    parser.add_argument("--response_chance",    dest="response_chance", nargs='?', default=0, type=float)

    parser.add_argument("--reply",              dest="reply", nargs='?', default=0, type=int,
                        help="Set to 1 if you want to reply, default is 0.")

    parser.add_argument("--max_history",        dest="max_history", nargs='?', default=4, type=int)

    parser.add_argument("--whitelist",          dest="whitelist", nargs='?', default=0, type=int)

    parser.add_argument("--top-k",              dest="top_k", nargs='?', default=40, type=int,
        help="Top-k, https://docs.cohere.ai/token-picking/")
    parser.add_argument("--top-p",              dest="top_p", nargs='?', default=0.9, type=float,
        help="Top-p, https://docs.cohere.ai/token-picking/")
    parser.add_argument("--temperature",        dest="temperature", nargs='?', default=0.8, type=float)

    parser.add_argument("--model",              dest="model", nargs='?', default="default", type=str,
        help="What model to use. Default is DialoGPT, set to a valid huggingface model from https://huggingface.co/models to use a custom model.")

    parser.add_argument("--local",              dest="local", nargs='?', default=False, type=bool,
        help="To add the the model paramater, is it a local file?")

    # console args
    parser.add_argument("--bots",               dest="bots", nargs='?', default=1, type=int, help="Set to 2 to have 2 chatbots talking to each other.")

    args, unknown = parser.parse_known_args(sys.argv)
    return args