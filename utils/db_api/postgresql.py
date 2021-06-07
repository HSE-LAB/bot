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
        sql = """
        CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        date VARCHAR(255) NOT NULL ,
        quantity INT NOT NULL,CHECK(quantity >= 0),
        product_id INT NOT NULL,
        sum INT NOT NULL,CHECK(sum >= 0),
        buyer INT NOT NULL,CHECK(buyer >= 0));

        -- Создание триггерной функции  
        CREATE FUNCTION trigger_for_date() RETURNS trigger AS $trigger_for_date$
            BEGIN
            NEW.date = nvl(NEW.date, current_date);
            return NEW;
        END;
        $trigger_for_date$ LANGUAGE  plpgsql;
        
        -- Создание триггера
        CREATE TRIGGER trigger_date
        BEFORE INSERT ON orders FOR EACH ROW
        EXECUTE PROCEDURE trigger_for_date()
        """
        await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT NOT NULL UNIQUE PRIMARY KEY,  
        fio VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL);
        """
        await self.execute(sql, execute=True)

    async def create_table_products(self):
        sql = """
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
        CREATE INDEX category_index ON products (category);
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
        sql = "INSERT INTO orders (date, quantity, product_id,sum,buyer) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(sql, date, quantity, product_id, sum, buyer, fetchrow=True)

    async def add_user(self, telegram_id, fio, address, phone):
        sql = "INSERT INTO users (telegram_id, fio, address, phone) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, telegram_id, fio, address, phone, fetchrow=True)

    async def select_all_categories(self):
        sql = 'select distinct category from products'
        return await self.execute(sql, fetch=True)

    async def select_products_from_category(self, category):
        sql = f"select distinct * from products where category='{category}'"
        return await self.execute(sql, fetch=True)

    async def select_product_by_id(self, product_id):
        sql = f"select distinct * from products where products.id='{product_id}'"
        return await self.execute(sql, fetch=True)

    async def select_product_flavour_by_id(self, product_id):
        sql = f"select distinct products.flavour from products where products.id='{product_id}'"
        return await self.execute(sql, fetch=True)

    async def select_product_by_name_flavour(self, name, flavour):
        sql = f"select distinct products.id from products where products.name='{name}' and products.flavour='{flavour}'"
        return await self.execute(sql, fetch=True)

    async def select_user_orders(self, telegram_id):
        sql = f"select distinct orders.date, orders.quantity, orders.product_id, orders.sum, orders.buyer " \
              f"from orders,users " \
              f"where orders.buyer = '{telegram_id}' "
        return await self.execute(sql, fetch=True)

    async def select_user_name_by_tg_id(self, telegram_id):
        sql = f"SELECT distinct users.fio FROM users WHERE users.telegram_id = '{telegram_id}' "
        return await self.execute(sql, fetch=True)

    async def update_user_name(self, telegram_id, new_fio):
        sql = f"UPDATE users SET fio = '{new_fio}' WHERE users.telegram_id = '{telegram_id}'"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_order_by_date(self, order_date):
        await self.execute(f"DELETE FROM orders WHERE orders.date = '{order_date}';", execute=True)

    async def delete_all_user_orders(self, telegram_id):
        await self.execute(f"DELETE FROM orders WHERE buyer = '{telegram_id}';", execute=True)

    async def drop_products(self):
        await self.execute("DROP TABLE products", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

    async def drop_orders(self):
        await self.execute("DROP TABLE orders", execute=True)

    async def drop_all(self):
        await self.execute("DROP TABLE orders", execute=True)
        await self.execute("DROP TABLE users", execute=True)
        await self.execute("DROP TABLE products", execute=True)

    async def delete_database(self):
        await self.execute(f"DROP DATABASE {self.dbname}")
        del self


# Все функции должны быть реализованы как хранимые процедуры. 