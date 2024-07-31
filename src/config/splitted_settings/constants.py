from pathlib import Path

BASE_DIR = BASE_DIR = Path(__file__).resolve().parent.parent

PAGINATION_AMOUNT = 8
BREADCRUMBS_HOME_LABEL = "Главная страница"
USER_CHOICE_PRINTY_ID = "user_choice_printy_id"
USER_CHOICE_STAMP_ID = "user_choice_stamp_id"
STAMP_ID_QUERY_PARAM = "stamp_id"
# Константа для hostname/sitemap.xml
SITE_ID = 1
# -------------------------------------------------------------------IMAGE-EDIT
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600
IMAGE_SIZE_IN_PIXELS = (600, 600)
TEXT_POSITION = (10, 10)  # from right bottom corner
TEXT_COLOR = (196, 207, 249, 53)  # Red, Green, Blue, Alpha(transparency)
FONT_SIZE = 32
WATERMARK_TEXT = "Печати-Архангельск.рф"
USE_WATERMARK_FILE = False
relative_path_to_watermark = "./docs/images/watermark.png"
WATERMARK_PATH = str(BASE_DIR / relative_path_to_watermark)
IMAGE_FORMAT = "PNG"
IMAGE_COLOR = "gray"
FONT = str(BASE_DIR / "static" / "fonts" / "DejaVuSans.ttf")
# ------------------------------------------------------------------------TITLE
TITLE = "Печати-Архангельск.рф"
INDEX_TITLE = "Главная страница"
ABOUT_CONTACTS_TITLE = "Контакты"
PRINTY_TITLE = "Группы оснасток"
ORDER_TITLE = "Оформление заказа"
ORDER_CREATED = "Заказ оформлен."
# -----------------------------------------------------------------BUTTONS-TEXT
ABOUT_GROUP = "Подробнее о группе"
ABOUT_STAMP = "Подробнее о печати"
ABOUT_PRINTY = "Подробнее о оснастке"
BUTTON_CHOICE_PRINTY = "Выбрать оснастку"
BUTTON_MAKE_ORDER = "Сделать заказ"
BUTTON_WRONG_PRINTY = "Оснастка не подходит под выбранную печать"
# -------------------------------------------------------BREADCRUMBS-HOME-LABEL
PRINTY_LABEL = "Группы оснасток"
# -------------------------------------------------------------BREADCRUMBS-PATH
PRINTY_PATH = "/printy/"
# --------------------------------------------------------------------TEMPLATES
INDEX_TEMPLATE = "mainapp/index.html"
ITEM_DETAIL_TEMPLATE = "mainapp/item_details.html"
ORDER_FORM_TEMPLATE = "mainapp/order_form.html"
ORDER_SUCCESS_TEMPLATE = "mainapp/order_success.html"
NEW_ORDER_EMAIL_TEMPLATE = "email/admin_new_order_info.html"
# -----------------------------------------------------------------CRISPY-FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# ------------------------------------------------------------------FACTORY-BOY
FIXTURES_LANGUAGE = "ru_Ru"
MIX_PRICE = 100
MAX_PRICE = 2000
SENTENCE_LEN = 3
PRINTY_PER_STAMP = 4
FIELDS_PER_GROUP = 4
GROUP_COLOR = "gray"
ITEM_COLOR = "black"
