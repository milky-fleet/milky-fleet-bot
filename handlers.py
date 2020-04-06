import requests
import datetime
import constants


def start_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send /help to checkout supported commands.")


def help_handler(update, context):
    text = 'Supported commands:\n' + \
           '/price SYMBOL: Show current price of the SYMBOL currency. Eg. /price BTC.\n' + \
           '/change SYMBOL GRANULARITY: Show last GRANULARITY change (between open and close price) SYMBOL currency. Eg. /change BTC 1m.\n' + \
           '/alarmstart SYMBOL GRANULARITY THRESHOLD Create an alarm if the last GRANULARITY' + \
           'change (between open and close price) of SYMBOL currency exceeds THRESHOLD. Eg. /alarmstart BTC 1m 20.\n' +\
           '/alarmstop ALERT_ID Stop the corresponding alarm(s). Eg. /alarmstop 1.\n' + \
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
    chat_id, symbol, granularity, threshold = context.job.context
    print(chat_id, symbol, granularity, threshold)
    change, vol = get_change(symbol, int(granularity))
    if vol >= float(threshold):
        alarm_text = "{} last {} change is: {:.2%} and volume is: {:.2f}".format(symbol, constants.SUPPORTED_GRANULARITY_WORD[granularity], change, vol)
        context.bot.send_message(chat_id=chat_id, text=alarm_text)

def callback_timer(update, context):
    texts = update.message.text.split()
    if len(texts) < 4:
        usage_text = 'Usage: /alarmstart SYMBOL GRANULARITY THRESHOLD Create an alarm if the last GRANULARITY ' + \
        'change (between open and close price) of SYMBOL currency exceeds THRESHOLD. Eg. /alarmstart BTC 1m 20'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=usage_text)
        return
    symbol = texts[1].upper()
    if symbol not in constants.SUPPORTED_SYMBOLS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=symbol + " is not supported.")
        return
    text_gran = texts[2]
    if text_gran not in constants.SUPPORTED_GRANULARITY_NUMBER.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_gran + " is not supported.")
        return
    granularity = constants.SUPPORTED_GRANULARITY_NUMBER[text_gran]
    threshold = texts[3]
    name = symbol + '_' + str(granularity) + '_' + threshold
    if name in context.user_data.keys():
        update.message.reply_text(
            'This alert was already set! Use /alarmstop {} to kill it'.format(context.user_data[name]))
    else:
        if 'num_of_jobs' not in context.user_data.keys():
            context.user_data['num_of_jobs'] = 1
        else:
            context.user_data['num_of_jobs'] += 1

        job_id = context.user_data['num_of_jobs']
        job = context.job_queue.run_repeating(callback_alarm, 60, context=[update.message.chat_id, symbol, granularity, threshold], name = job_id)
        context.user_data[str(job_id)] = job
        context.user_data[name] = job_id
        context.bot.send_message(chat_id=update.message.chat_id,
                      text='Alert Starting! Alert ID {}.'.format(context.user_data['num_of_jobs']))

def stop_alarm(update, context):
    texts = update.message.text.split()
    if len(texts) < 2:
        usage_text = 'Usage: /alarmstop ALERT_ID Stop the corresponding alarm(s). Eg. /alarmstop 1'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=usage_text)
    job_ids = texts[1:]
    for job_id in job_ids:
        if job_id in context.user_data.keys():
            context.bot.send_message(chat_id=update.message.chat_id,
                              text='Alert {} Stoped!'.format(job_id))
            context.user_data[job_id].schedule_removal()
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                              text='Alert {} does not exist'.format(job_id))            

def change_handler(update, context):
    texts = update.message.text.split()
    if len(texts) < 3:
        usage_text = 'Usage: /change SYMBOL GRANULARITY Show last GRANULARITY change (between open and close price) SYMBOL currency. Eg. /change BTC 1m'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=usage_text)
        return
    symbol = texts[1].upper()
    if symbol not in constants.SUPPORTED_SYMBOLS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=symbol + " is not supported.")
        return
    text_gran = texts[2]
    if text_gran not in constants.SUPPORTED_GRANULARITY_NUMBER.keys():
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_gran + " is not supported.")
        return
    granularity = constants.SUPPORTED_GRANULARITY_NUMBER[text_gran]

    change, vol = get_change(symbol, granularity)
    text = "{} last {} change is: {:.2%} and volume is: {:.2f}".format(symbol, constants.SUPPORTED_GRANULARITY_WORD[granularity], change, vol)
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
