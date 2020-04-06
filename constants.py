SUPPORTED_SYMBOLS = {'NIO', 'BGN', 'GMD', 'YER', 'MGA', 'SAR', 'CVE', 'REP', 'HNL', 'MZN', 'SLL', 'IQD', 'AFN', 'HRK',
                     'BAM', 'GBP', 'EGP', 'EOS', 'MMK', 'XAF', 'BTC', 'VUV', 'PYG', 'LVL', 'ETC', 'ETB', 'LTL', 'BOB',
                     'MAD', 'KRW', 'LTC', 'ISK', 'KGS', 'STD', 'ATOM', 'ARS', 'LSL', 'VND', 'BIF', 'MKD', 'NPR', 'PEN',
                     'BZD', 'TND', 'AED', 'BMD', 'MRO', 'FJD', 'UYU', 'XOF', 'BRL', 'AOA', 'XPF', 'BHD', 'TWD', 'LYD',
                     'TRY', 'XRP', 'MWK', 'QAR', 'ZWL', 'BTN', 'GGP', 'KZT', 'LKR', 'THB', 'AUD', 'NOK', 'UGX', 'ZRX',
                     'MYR', 'DJF', 'LINK', 'BDT', 'KHR', 'NGN', 'CUC', 'MUR', 'FKP', 'COP', 'XLM', 'ALL', 'AZN', 'GEL',
                     'NZD', 'TTD', 'XTZ', 'BND', 'DASH', 'KYD', 'PGK', 'IDR', 'BAT', 'SEK', 'VES', 'RUB', 'DAI', 'SGD',
                     'SOS', 'GNF', 'RSD', 'BYR', 'GIP', 'KNC', 'MDL', 'SBD', 'ZAR', 'GHS', 'AWG', 'SZL', 'EUR', 'JOD',
                     'SCR', 'BBD', 'PHP', 'JMD', 'MNT', 'EEK', 'LAK', 'CRC', 'RON', 'SHP', 'VEF', 'XAU', 'ZMW', 'INR',
                     'ZEC', 'PAB', 'TOP', 'KES', 'GYD', 'HTG', 'NAD', 'UAH', 'KWD', 'XAG', 'AMD', 'XPD', 'SSP', 'DZD',
                     'CLF', 'XCD', 'XDR', 'USDC', 'USD', 'TZS', 'CDF', 'LRD', 'HUF', 'CNY', 'HKD', 'WST', 'ANG', 'XPT',
                     'TMT', 'CZK', 'ETH', 'BSD', 'ZMK', 'DOP', 'GTQ', 'KMF', 'UZS', 'JEP', 'OXT', 'BYN', 'ILS', 'CAD',
                     'SVC', 'PLN', 'TJS', 'CLP', 'RWF', 'PKR', 'SRD', 'MOP', 'MXN', 'LBP', 'BSV', 'CNH', 'DKK', 'ERN',
                     'MTL', 'CHF', 'BCH', 'BWP', 'JPY', 'IMP', 'MVR', 'OMR', 'SAI'}

SUPPORTED_GRANULARITY_WORD = {
    60: 'one minute', 
    300: 'five minutes',
    900: 'fifteen minutes',
    3600 : 'one hour',
    21600 : 'six hours',
    86400 : 'one day'
}

SUPPORTED_GRANULARITY_NUMBER = {
    '1m': 60, 
    '5m': 300,
    '15m': 900,
    '1h': 3600,
    '6h': 21600,
    '1d': 86400
}