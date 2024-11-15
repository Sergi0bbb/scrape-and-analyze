# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
from web_site_analysis import settings

DB_NAME = settings.DB_NAME
TABLE_NAME = settings.TABLE_NAME


class WebSiteAnalysisPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        data = (
            adapter.get("title"),
            adapter.get("publish_date"),
            adapter.get("experience"),
            adapter.get("company"),
            adapter.get("company_description"),
            adapter.get("place"),
            adapter.get("salary"),
            adapter.get("technologies"),
        )

        self.cursor.execute(
            f"""
            INSERT INTO {TABLE_NAME} (
                title,
                publish_date,
                experience,
                company,
                company_description,
                place,
                salary,
                technologies
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data,
        )
        return item

    def open_spider(self, spider):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                title TEXT,
                publish_date DATE,
                experience INT,
                company TEXT,
                company_description TEXT,
                place TEXT,
                salary INT,
                technologies TEXT
            )
            """
        )
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
