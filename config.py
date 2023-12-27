api_id = 27218646 # Ваш апи айди
api_hash='ad50272cdbda3eedd301bfb19f3f3954' # Ваш апи ключ
# Инструкция по получению: https://telegra.ph/Sozdayom-paru-api-idhash-dlya-lovca-chekov-11-03

channel = -1002065627438 # Айди канала с логами об активированных чеках. Если вы хотите указать пуличный канал, то введите 'тег без @', Например

avto_vivod = False # Если данные параметр True, то скрипт раз в сутки будет переводить деньги с помощью чека на указанный аккаунт. Чтобы отключить укажите False, например avto_vivod = False
avto_vivod_tag = 'ваш_тег' # Тег аккаунта(без @), куда раз в сутки будет отправляться чек со всеми собранными средствами. Например avto_vivod_tag = 'absolutely_enough'

avto_otpiska = True # Если данные параметр True, то скрипт будет автоматически выходить из каналов, которе не публиковали чеки в течении суток. Чтобы отключить укажите False, например avto_otpiska = False

anti_captcha = True # Если параметр True, то скрипт будет автоматически разгадывать каптчу для CryptoBot. Чтобы отключить укажите False, например anti_captcha = False

ocr_api_key = 'K86292007688957' # Инструкция по получению: https://telegra.ph/Poluchenie-OCR-API-KEY-11-03

# https://t.me/lovec_checkov