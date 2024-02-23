from src import ExcelProcessor, Scraper


def main():
    scraper = Scraper()

    excel_processor = ExcelProcessor("USA Services.xlsx", scraper)

    excel_processor.process_links_and_get_emails()

    scraper.close()


if __name__ == "__main__":
    main()
