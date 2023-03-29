import inspect

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from telegram import ReplyKeyboardRemove, Update, ParseMode
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ContextTypes,
    Filters,
    MessageHandler,
    PollAnswerHandler, CallbackQueryHandler,
)

from src.bot.core.helpers import get_or_create_user
from src.bot.core.parse_city import parse_cloth
from src.bot.core.telegram import dp
from src.bot.core.utils import get_cloth_msg
from src.bot.modules.base.keyboard import build_inlines_menu
from src.cloth.models import Profession


def start(update: Update, context: CallbackContext) -> None:
    user = get_or_create_user(update.effective_user)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {user.name}. Напиши профессию для поиска",
    )


def get_cloth(update: Update, context: CallbackContext) -> None:



    professions = (
        Profession.objects.prefetch_related("cloth").annotate(
            similarity=TrigramSimilarity("name", update.message.text)
        )
        .filter(similarity__gt=0.2)
        .order_by("-similarity")
    )

    professions_contain = Profession.objects.filter(name__icontains=update.message.text)

    professions = professions.union(professions_contain)

    if not professions.exists():
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Профессия не найдена",
        )
    professions = professions.values_list("name", flat=True)
    professions_list = list()
    for profession_el in professions:
        if len(profession_el) > 25:
            professions_list.append(profession_el[:25])
        else:
            professions_list.append(profession_el)
    reply_markup = build_inlines_menu(buttons=professions_list, pattern="profession::")

    update.message.reply_text(
        reply_markup=reply_markup,
        text="Профессии похожие на ваш запрос",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    # for profession in professions:
    #     cloths = get_cloth_msg(cloths=profession.cloth.all().values("name", "count"))
    #     msg = f"""Название провессии: {profession.name} \n""" + cloths
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=inspect.cleandoc(msg),
    #     )


def get_cloth_on_button(update: Update, context: ContextTypes) -> None:
    """Выдача професии по нажатию кнопки"""
    _, profession = update.callback_query.data.split("::")

    professions = Profession.objects.filter(name__icontains=profession)

    for profession in professions:
        cloths = get_cloth_msg(cloths=profession.cloth.all().values("name", "count"))
        msg = f"""Название провессии: {profession.name} \n""" + cloths
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=inspect.cleandoc(msg),
        )



dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(get_cloth_on_button, pattern="^profession::"))
dp.add_handler(MessageHandler(Filters.text & (~Filters.command), get_cloth))
