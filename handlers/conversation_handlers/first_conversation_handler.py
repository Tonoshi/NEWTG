from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

GENDER, PHOTO = range(2)


class FirstConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begin', cls.begin)],
            states={
                GENDER: [MessageHandler(filters.Regex('^(Boy|Girl)$'), cls.gender)],
                PHOTO: [MessageHandler(filters.PHOTO, cls.photo)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Boy'), KeyboardButton('Girl')],
        ]
        reply_text = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Hello {update.effective_user.first_name}! Are you a Boy or a Girl?',
                                        reply_markup=reply_text)

        return GENDER

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'You are a {update.message.text}. Share your photo, please!', reply_markup=ReplyKeyboardRemove())

        return PHOTO

    @staticmethod
    async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Thank you for your photo!', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END