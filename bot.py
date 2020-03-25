import argparse
import logging
import sys

from telegram.ext import CommandHandler, Updater

import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def run_bot(args):
    updater = Updater(token=args.bot_token, use_context=True)
    bot = updater.bot
    logging.info(f'Started {bot.first_name} bot, bot username: {bot.username}')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', handlers.start_handler))
    dispatcher.add_handler(CommandHandler('help', handlers.help_handler))
    dispatcher.add_handler(CommandHandler('price', handlers.price_handler))

    updater.start_polling()


def validate_args(args):
    if args.bot_token is None or args.bot_token == '':
        print("--bot_token is required.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--bot_token", help="Token of Telegram bot")
    args = parser.parse_args()
    validate_args(args)
    run_bot(args)
