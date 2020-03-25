import requests

import constants


def start_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send /help to checkout supported commands.")


def help_handler(update, context):
    text = 'Supported commands:\n' + \
           '/price SYMBOL: Show current price of the SYMBOL currency. Eg. /price BTC\n' + \
           '\n' + \
           'Github: github.com/milky-fleet/milky-fleet-bot\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def price_handler(update, context):
    # update.message.text: '/price btc'
    symbol = update.message.text[7:].strip().upper()
    if symbol == '':
        usage_text = 'Usage: /price SYMBOL Show current price of the SYMBOL currency. Eg. /price BTC'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=usage_text)
        return
    elif symbol not in constants.SUPPORTED_SYMBOLS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=symbol + " is not supported.")
        return
    text = "Current " + symbol + " price is: $" + get_price(symbol)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_price(symbol):
    res = requests.get('https://api.coinbase.com/v2/exchange-rates')
    price = 1 / float(res.json()['data']['rates'][symbol])
    return str(price)
