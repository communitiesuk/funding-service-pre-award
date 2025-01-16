from datetime import datetime

from flask_babel import format_datetime, gettext


def datetime_format_respect_lang(value: datetime) -> str:
    """
    Format a date-time string to match the GOV.UK style guide.

    This function takes a date-time string in the format "%Y-%m-%dT%H:%M:%S" and
    returns it in a human-readable format that adheres to the guidelines provided by
    the GOV.UK style guide.

    Specifically:
    - The time "00:00" is represented as "midnight".
    - The time "12:00" is represented as "midday".
    - All other times are in the format "HH:MMam/pm" without leading zeros in the hour.

    Parameters:
    - value (str): The date-time string to be formatted.
                   Example: "2020-01-01T12:00:00"

    Returns:
    - str: A string representing the date-time in the GOV.UK recommended style.

    Reference:
    - https://www.gov.uk/guidance/style-guide/a-to-z-of-gov-uk-style#times
    """

    if value.time().hour == 0 and value.time().minute == 0:
        time_str = gettext("midnight")
    elif value.time().hour == 12 and value.time().minute == 0:
        time_str = gettext("midday")
    else:
        time_str = value.strftime("%I:%M%p").lstrip("0").lower()

    formatted_date = format_datetime(value, format="dd MMMM yyyy ")
    formatted_date += gettext("at")
    formatted_date += " " + time_str
    return formatted_date
