import logging

from telegram import Update
from telegram.error import ChatMigrated
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

TOKEN = '6079606697:AAECpIYAClhWjSrOzAOzTCxpp1wZlC412ng'
ORIGIN_GROUP_ID = -970476227  # Substitua pelo ID do grupo de origem

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GroupHandler:
    def __init__(self, target_group_id):
        self.target_group_id = target_group_id

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text('Bot iniciado!')

    def get_chat_id(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        update.message.reply_text(f'O ID deste chat é: {chat_id}')

    def copy_message(self, update: Update, context: CallbackContext):
        message = update.message
        if message.chat_id == ORIGIN_GROUP_ID:
            try:
                context.bot.send_message(
                    chat_id=self.target_group_id, text=message.text)
            except ChatMigrated as e:
                new_chat_id = e.new_chat_id
                update.message.reply_text(
                    f'O grupo foi migrado para um supergrupo. Novo ID do chat: {new_chat_id}')
                self.target_group_id = new_chat_id
                context.bot.send_message(
                    chat_id=self.target_group_id, text=message.text)


def main():
    target_group_id = -964537514  # Substitua pelo ID do grupo de destino
    group_handler = GroupHandler(target_group_id)

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', group_handler.start))
    dp.add_handler(CommandHandler('getidsbot', group_handler.get_chat_id))
    dp.add_handler(MessageHandler(Filters.text & ~
                   Filters.command, group_handler.copy_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
