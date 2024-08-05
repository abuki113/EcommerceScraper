# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging
import hashlib

class customImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        image_perspective = item["name"].lower().replace(" ", "_")
        image_filename = f"ecommerce_project/data/images{image_perspective}.jpg"

        return image_filename


## Save to MySQL Database
import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '******',
        database = 'books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS products(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            description text,
            image_path VARCHAR(255),
            PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        """Defines, inserts statement and insert the data to the database"""
        
        # Define insert statement
        self.cur.execute(""" insert into books (
            name, 
            description, 
            image_path
            ) values (
            %s,
            %s,
            %s
            )""", (
            item["name"],
            item["description"],
            item["images"]["path"]
        ))
        ## Execute insert of data into database
        self.conn.commit()

        def close_spider(self, spider):
            """Close cursor & connection to database""" 
            self.cur.close()
            self.conn.close()


# pipelines.py

import psycopg2

class SaveToPostgresPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = '******' # your password
        database = 'books'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id serial PRIMARY KEY, 
            name VARCHAR(255),
            description text,
            image_path VARCHAR(255)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            name, 
            description, 
            image_url
            ) values (
                %s,
                %s,
                %s
                )""", (
            item["name"],
            item["description"],
            item["images"]["path"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
