from openpyxl import Workbook


def generate_report_1(workbook: Workbook) -> None:
    sheet = workbook.create_sheet(title="Report 1")

    sheet.append(["ID", "Name", "Value"])

    sample_data = [
        (1, "Item A", 100),
        (2, "Item B", 200),
        (3, "Item C", 300),
    ]

    for row in sample_data:
        sheet.append(row)


def generate_report_2(workbook: Workbook) -> None:
    sheet = workbook.create_sheet(title="Report 2")

    sheet.append(["Category", "Count", "Total"])

    sample_data = [
        ("Category X", 5, 1500),
        ("Category Y", 3, 900),
        ("Category Z", 7, 2100),
    ]

    for row in sample_data:
        sheet.append(row)
