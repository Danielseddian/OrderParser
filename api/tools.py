import httplib2
import requests

from googleapiclient.discovery import build
from OrderParser import settings
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from typing import Union, Dict, Tuple, List

SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)
ACCESS_JSON_TYPE_ERROR = "Запрос к Google sheets осуществляется с использованием JSON словаря или пути к .json файлу"
SH_RANGE = "Лист1!A1:Z999999"
UNEXPECTED_CURRENCY_ERROR = 'Не удалось найти валюту {}. Необходимо указать валюту в формате: "USD"'


def make_google_sheets_request(
    access_json: Union[str, Dict] = settings.GOOGLE_ACCESS_JSON,
    scopes: Union[Tuple, List] = SCOPES,
):
    """
    Make API-request from Google sheets
    :param access_json: Token's dictionary or token's .json file path for access to Google sheets
    :param scopes: Access levels
    :return: Google sheet's prepared request
    """
    if isinstance(access_json, dict):
        cred_service = ServiceAccountCredentials.from_json_keyfile_dict(access_json, scopes).authorize(httplib2.Http())
    elif isinstance(access_json, str):
        cred_service = ServiceAccountCredentials.from_json_keyfile_name(access_json, scopes).authorize(httplib2.Http())
    else:
        raise TypeError(ACCESS_JSON_TYPE_ERROR)
    return build("sheets", "v4", http=cred_service)


def read_google_sheet(
    sheet_id: str = settings.ORDERS_GOOGLE_SHEET,
    sh_range: str = SH_RANGE,
    google_request=None,
    access_json: Union[str, Dict] = settings.GOOGLE_ACCESS_JSON,
    scopes: Union[Tuple, List] = SCOPES,
) -> [[]]:
    """
    Get response and read Google sheet
    :param sheet_id: Execution sheet id
    :param sh_range: Execution spreadsheet range
    :param google_request: Google sheet's prepared request
    :param access_json: Token's dictionary or token's .json file path for access to Google sheets
    :param scopes: Access levels
    :return: Spreadsheet array
    """
    if not google_request:
        google_request = make_google_sheets_request(access_json, scopes)
    return google_request.spreadsheets().values().get(spreadsheetId=sheet_id, range=sh_range).execute().get("values")


def get_exchange(currency: str = "USD") -> float:
    """
    Get current currency exchange rate from Central Bank of Russian Federation
    :param currency: Expected currency
    :return: The current currency exchange rate or "0.0", if the Central Bank's response is not received
    """
    try:
        return requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()["Valute"][currency]["Value"]
    except IndexError:
        raise ValueError(UNEXPECTED_CURRENCY_ERROR)
    except Exception:
        return 0.0


def notify(text: str, chat_id: str = settings.TELEGRAM_CHAT_ID, token: str = settings.TELEGRAM_TOKEN):
    try:
        Bot(token=token).send_message(chat_id, text)
    except Exception as exc:
        return exc.__repr__()
