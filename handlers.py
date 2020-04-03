import requests
import datetime
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
    text = "Current {} price is: ${:.2f}".format(symbol, float(get_price(symbol)))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_price(symbol):
    res = requests.get('https://api.coinbase.com/v2/exchange-rates')
    price = 1 / float(res.json()['data']['rates'][symbol])
    return str(price)


def callback_alarm(context):
    change, vol = get_change('BTC', 60)
    if vol >= 10:
        alarm_text = 'BTC last one minute change is: {:.2%} and volume is: {:.2f}'.format(change, vol)
        context.bot.send_message(chat_id=context.job.context, text=alarm_text)


def callback_timer(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                      text='Alert Starting!')
    context.job_queue.run_repeating(callback_alarm, 60, context=update.message.chat_id)

def stop_timer(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                      text='Alert Stoped!')
    context.job_queue.stop()

def change_handler(update, context):
    texts = update.message.text.split()
    if len(texts) < 3:
        usage_text = 'Usage: /change SYMBOL GRANULARITY Show last one minute change (between open and close price) SYMBOL currency. Eg. /change BTC 60'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=usage_text)
        return
    symbol = texts[1].upper()
    granularity = texts[2]
    if symbol not in constants.SUPPORTED_SYMBOLS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=symbol + " is not supported.")
        return
    if granularity not in constants.SUPPORTED_GRANULARITY.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=granularity + " is not supported.")
        return
    change, vol = get_change(symbol, granularity)
    text = "{} last {} change is: {:.2%} and volume is: {:.2f}".format(symbol, constants.SUPPORTED_GRANULARITY[granularity], change, vol)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def get_change(symbol, granularity):
    start_time = datetime.datetime.now().isoformat()
    res = requests.get('https://api.pro.coinbase.com/products/{}-USD/candles?start={}&granularity={}'.format(symbol, start_time, granularity))
    res = res.json()
    open_rate = res[0][3]
    close_rate = res[0][4]
    vol = res[0][5]
    change = (close_rate/open_rate - 1)
    return change, vol
