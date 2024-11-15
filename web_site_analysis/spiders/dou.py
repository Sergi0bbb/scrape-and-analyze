import re
from datetime import date

import scrapy
from scrapy import Request
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from web_site_analysis.collections import MONTHS_UA, TECHNOLOGIES


class Spider(scrapy.Spider):
    name = "dou"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    def parse(self, response: Response, **kwargs) -> dict:
        html = self._load_all_vacancies(response.url)
        response = response.replace(body=html)

        for vacancy in response.css(".l-vacancy"):
            yield Request(
                url=vacancy.css(".title .vt::attr(href)").get(),
                callback=self._parse_detail_url,
                meta={
                    "title": vacancy.css(".title .vt::text").get(),
                    "publish_date": self._convert_ukr_date(
                        vacancy.css(".date::text").get()
                    ),
                    "company": vacancy.css(".title > strong > a::text")
                    .get()
                    .replace("\xa0", ""),
                }
            )

    @classmethod
    def _load_all_vacancies(cls, url: str) -> str:
        chrome_options = Options()
        chrome_options.headless = True

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            load_more = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, ".more-btn > a")
                )
            )
            while load_more.is_displayed():
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    load_more
                )
                load_more.click()
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, ".more-btn > a")
                    )
                )
                load_more = driver.find_element(
                    By.CSS_SELECTOR, ".more-btn > a"
                )
        except Exception as e:
            print(f"Error occurred while loading more jobs: {e}")
        finally:
            page_source = driver.page_source
            driver.quit()

        return page_source

    def _parse_detail_url(self, response: Response) -> dict:
        salary = response.css(".salary::text").re_first(
            r"\$?\s*(\d+(\.\d{1,2})?)"
        )
        description = response.css(".vacancy-section").get()

        yield {
            "title": response.meta["title"],
            "publish_date": response.meta["publish_date"],
            "company": response.meta["company"],
            "company_description": response.css(".l-t::text")
            .get()
            .replace("\xa0", "")
            .strip(),
            "experience": self._parse_experience(description),
            "place": response.css(".sh-info .place::text").get(),
            "salary": float(salary) if salary else salary,
            "technologies": ", ".join(self._parse_technologies(description)),
        }

    @classmethod
    def _convert_ukr_date(cls, publish_date_str: str) -> date:
        day, month = publish_date_str.split()
        month_num = MONTHS_UA.get(month, 0)
        return date(date.today().year, month_num, int(day))

    @classmethod
    def _parse_experience(cls, description: str) -> int | None:
        pattern = (
            r"(\d+)\+?\s*(?:роки досвіду|років досвіду|"
            r"years of experience|years of)"
        )
        matches = re.findall(pattern, description, re.IGNORECASE)

        if matches:
            years_of_experience = max(
                int(match) for match in matches if int(match) < 15
            )
            return years_of_experience

        return None

    @classmethod
    def _parse_technologies(cls, description: str) -> list[str]:
        return [
            tech for tech in TECHNOLOGIES if
            re.search(rf"\b{tech}\b", description, re.IGNORECASE)
        ]
