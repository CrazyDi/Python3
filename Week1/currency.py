from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):

    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", params={"date_req": date})  # Использовать переданный requests
    soup = BeautifulSoup(response.content, "xml")
    if cur_from == "RUR":
        value_from = Decimal(1.0)
        nominal_from = Decimal(1.0)
    else:
        value_from = Decimal(str(soup.find("CharCode", text=cur_from).find_next_sibling('Value').string).replace(",", "."))
        nominal_from = Decimal(str(soup.find("CharCode", text=cur_from).find_next_sibling('Nominal').string).replace(",", "."))

    if cur_to == "RUR":
        value_to = Decimal(1.0)
        nominal_from = Decimal(1.0)
    else:
        value_to = Decimal(
            str(soup.find("CharCode", text=cur_to).find_next_sibling('Value').string).replace(",", "."))
        nominal_to = Decimal(
            str(soup.find("CharCode", text=cur_to).find_next_sibling('Nominal').string).replace(",", "."))

    result = ((amount * value_from) / nominal_from) / value_to * nominal_to
    result = result.quantize(Decimal(".0001"))

    return result  # не забыть про округление до 4х знаков после запятой

