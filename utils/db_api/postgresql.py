from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False,
                      fetchall: bool = False,
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                
            return result
    
    async def create_table_orders(self):
        sql="""
        CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        date VARCHAR(255) NOT NULL ,
        quantity INT NOT NULL,CHECK(quantity >= 0),
        product_id INT NOT NULL,
        sum INT NOT NULL,CHECK(sum >= 0),
        buyer INT NOT NULL,CHECK(buyer >= 0));
        """ 
        await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql="""
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fio VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL);
        """ 
        await self.execute(sql, execute=True)

    async def create_table_products(self):
        sql="""
        CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        flavour VARCHAR(255) NOT NULL,
        price INT NOT NULL,CHECK(price >= 0),
        name VARCHAR(255) NOT NULL,
        img_link VARCHAR(500) NOT NULL,
        category VARCHAR(255) NOT NULL);
        INSERT INTO products (flavour, price, name,img_link, category) VALUES('Клубника',100,'Мюсли','https://stat5.cdnbb8.com/upload/2012/2018-02/plkaz.jpg','Завтраки'); 
        INSERT INTO products (flavour, price, name, img_link,category) VALUES('Персик',50,'Протеиновый батончик','https://fitbar.ru/images/uploaded/article/5dfa1d92c8542.jpg','Снеки');
        INSERT INTO products (flavour, price, name,img_link, category) VALUES('Ваниль',500,'Протеиновый коктель','https://builderbody.ru/wp-content/uploads/2015/09/51.jpg','Напитки');
        INSERT INTO products (flavour, price, name,img_link, category) VALUES('Клубника',70,'Пастила','https://productplanet.ru/wp-content/uploads/2019/02/pastila-anons.jpg','Снеки');  
        """
        await self.execute(sql, execute=True)

    

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_order(self, date, quantity, product_id, sum, buyer):
        sql = "INSERT INTO users (date, quantity, product_id,sum,buyer) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(sql, date, quantity, product_id,sum,buyer, fetchrow=True)

    
    async def add_user(self, fio, address, phone):
        sql = "INSERT INTO users (fio, address, phone) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, fio, address, phone, fetchrow=True)

    async def select_all_categories(self):
        sql = 'select distinct category from products'
        return await self.execute(sql, fetch=True)
    
    
    
    
    async def select_products_from_category(self,category):
        sql = f"select distinct * from products where category='{category}'"
        return await self.execute(sql, fetch=True)


    # async def select_all_users(self):
    #     sql = "SELECT * FROM Users"
    #     return await self.execute(sql, fetch=True)

    # async def select_user(self, **kwargs):
    #     sql = "SELECT * FROM Users WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetchrow=True)

    # async def count_users(self):
    #     sql = "SELECT COUNT(*) FROM Users"
    #     return await self.execute(sql, fetchval=True)

    # async def update_user_username(self, username, telegram_id):
    #     sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
    #     return await self.execute(sql, username, telegram_id, execute=True)

    # async def delete_users(self):
    #     await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_products(self):
        await self.execute("DROP TABLE products", execute=True)