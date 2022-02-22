from sqlite3 import *
from data.config import DATABASE





class DBApi(object):

    def __init__(self) -> None:
        self.__conn: Connection = connect(DATABASE)
        self.__cur: Cursor = self.__conn.cursor()

    async def create_roles_table(self) -> None:
        """CREATE ROLES TABLE"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            roles(
                role TEXT PRIMARY KEY
            )
        ''')
        self.__conn.commit()

    async def create_users_table(self) -> None:
        """CREATE USER TABLES"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            users(
                user_id INTEGER PRIMARY KEY,
                role TEXT NOT NULL,
                FOREIGN KEY (role) REFERENCES roles(role)
            )
        ''')
        self.__conn.commit()

    async def create_categories_table(self) -> None:
        """CREATE CATEGORIES TABLE"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            categories(
                category TEXT PRIMARY KEY
            )
        ''')
        self.__conn.commit()

    async def create_subcategories_table(self) -> None:
        """CREATE SUBCATEGORIES TABLE"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            subcategories(
                subcategory TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                FOREIGN KEY (category) REFERENCES categories(category)
            )
        ''')
        self.__conn.commit()

    async def create_products_table(self) -> None:
        """CREATE PRODUCTS TABLE"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                media_id TEXT,
                price INTEGER NOT NULL,
                subcategory TEXT,
                FOREIGN KEY (subcategory) REFERENCES subcategories(subcategory)
            )
        ''')
        self.__conn.commit()

    async def check_user(self, user_id: int) -> bool:
        """CHECK USER EXISTS"""
        self.__cur.execute('''
            SELECT user_id
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        return bool(self.__cur.fetchone())

    async def add_new_user(self, user_id: int, role: str = "user") -> bool:
        """ADD NEW USER"""
        try:
            self.__cur.execute('''
                INSERT INTO users(
                    user_id,
                    role
                )
                VALUES(?, ?)
            ''', (user_id, role))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def change_user_role(self, user_id: int, new_role: str) -> None:
        """EDIT USER ROLE"""
        self.__cur.execute('''
            UPDATE users
            SET role = ?
            WHERE user_id = ?
        ''', (new_role, user_id))
        self.__conn.commit()

    async def add_category(self, category: str) -> bool:
        """ADD NEW CATEGORY"""
        print(category)
        try:
            self.__cur.execute('''
                INSERT INTO
                categories(
                    category
                )
                VALUES(?)
            ''', (category, ))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def add_subcategory(self, category: str, subcategory: str) -> bool:
        """ADD NEW SUBCATEGORY"""
        try:
            self.__cur.execute('''
                        INSERT INTO
                        subcategories(
                            category,
                            subcategory
                        )
                        VALUES(?, ?)
                    ''', (category, subcategory))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def add_product(self, title: str, description: str, price: int, subcategory: str, media_id: str = None) -> bool:
        """ADD PRODUCT TO SUBCATEGORY"""
        try:
            self.__cur.execute('''
                INSERT INTO products(
                    title,
                    description,
                    price,
                    media_id,
                    subcategory
                )
                VALUES(?, ?, ?, ?, ?)
            ''', (title, description, price, media_id, subcategory))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def get_subcategories(self, category: str = None) -> tuple:
        """GET ALL SUBCATEGORIES FOR CATEGORY"""
        if category:
            self.__cur.execute('''
                SELECT subcategory
                FROM subcategories
                WHERE category = ?
            ''', (category, ))
        else:
            self.__cur.execute('''
                SELECT subcategory
                FROM subcategories
            ''')
        return tuple([subcategory[0] for subcategory in self.__cur.fetchall()])

    async def get_all_roles(self) -> tuple:
        """GET ALL ROLES"""
        self.__cur.execute('''
            SELECT role
            FROM roles
        ''')
        return tuple([role[0] for role in self.__cur.fetchall()])

    async def get_all_admins(self) -> tuple:
        """GET ALL ADMINS FROM DATABASE"""
        self.__cur.execute('''
            SELECT user_id
            FROM users
            WHERE role = ?
        ''', ("admin", ))
        return tuple([admin[0] for admin in self.__cur.fetchall()])

    async def get_products(self, subcategory: str) -> tuple:
        """GET ALL PRODUCTS FOR SUBCATEGORY FROM DATABASE"""
        self.__cur.execute('''
            SELECT *
            FROM products
            WHERE subcategory = ?
        ''', (subcategory, ))
        return tuple(self.__cur.fetchall())

    async def get_product(self, product_id: int) -> tuple:
        """GET ONE PRODUCT FROM DATABASE"""
        self.__cur.execute('''
            SELECT *
            FROM products
            WHERE id = ?
        ''', (product_id, ))
        return tuple(self.__cur.fetchone())




    """Вывод всех ресторан"""
    async def get_restaurants(self) -> tuple:
        """GET ALL ROOT restaurants"""
        self.__cur.execute('''
            SELECT name_restaurants
            FROM restaurants
        ''')
        return tuple([category[0] for category in self.__cur.fetchall()])

    """Вывод вывод определенного ресторана"""
    async def get_current_restaurants(self, name_restaurants) -> list:
        request_all_menu = f'SELECT * FROM restaurants WHERE name_restaurants = "{name_restaurants[0]}"'
        result_request_all_menu = self.__cur.execute(request_all_menu).fetchall()
        return result_request_all_menu

    """Вывод всего меню на русском языке"""
    async def get_menu(self) -> tuple:
        """GET ALL menu"""
        self.__cur.execute('''
            SELECT *
            FROM menu
        ''')
        return tuple([menu[1] for menu in self.__cur.fetchall()])

    """Вывод меню на английском языке"""
    async def get_English_name_menu(self, name_product: str) -> tuple:
        """GET ALL menu"""
        self.__cur.execute(f'''
            SELECT English_name
            FROM menu
            WHERE name = ?
        ''', (name_product, ))
        return tuple([menu[0] for menu in self.__cur.fetchall()])

    """Вывод меню"""
    async def get_menu_product(self, name_table) -> list:
        request_all_menu = f'SELECT * FROM {name_table[0]}'
        result_request_all_menu = self.__cur.execute(request_all_menu).fetchall()
        return result_request_all_menu

    """Вывод определенного продукта"""
    async def get_current_product(self, name_table, name_product) -> list:
        request_current_menu = f"SELECT * FROM {name_table[0]} WHERE name = '{name_product}'"
        result_request_all_menu = self.__cur.execute(request_current_menu).fetchall()
        return result_request_all_menu


    """Добавление товара в меню"""
    async def sql_add_product(self, img, name_prod, description_sauces, price_sauces):
        """ADD NEW product"""
        try:
            self.__cur.execute('''
                INSERT INTO
                    combo(
                        img,
                        name,
                        description,
                        price
                    )
                VALUES(?, ?, ?, ?)
            ''', (img, name_prod, description_sauces, price_sauces))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Добавление купона"""
    async def sql_add_coupons(self, img, name_coupons, price):
        try:
            self.__cur.execute('''
                            INSERT INTO
                                coupons(
                                    img,
                                    name,
                                    price
                                )
                            VALUES(?, ?, ?)
                        ''', (img, name_coupons, price))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Вывод купонов"""
    async def sql_show_coupons(self) -> list:
        result = f"SELECT * FROM coupons"
        return self.__cur.execute(result).fetchall()




    """ПОЛЬЗОВАТЕЛЬ"""


    """Запись нового пользователя который хочет устроиться"""
    async def sql_add_user_career(self,user_id, lname, fname, age, phone,e_mail, city, subway, restaurant):
        """ADD NEW product"""
        try:
            self.__cur.execute('''
                INSERT INTO
                    career(
                        user_id,
                        lname,
                        fname,
                        age,
                        phone,
                        e_mail,
                        city,
                        subway,
                        restaurant
                    )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, lname, fname, age, phone, e_mail, city, subway, restaurant))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Получение id пользователя"""
    async def sql_user_id(self, user_id) -> list:
        result = f"SELECT user_id FROM career WHERE user_id = {user_id}"
        return self.__cur.execute(result).fetchall()

    async def sql_select_user_action(self, user_id) -> list:
        result = f"SELECT user_id FROM career WHERE user_id = {user_id}"
        return self.__cur.execute(result).fetchall()

    """оБНОВЛЕНИЕ ресторана В ТАБЛИЦЕ АКТИВНОСТЬ"""
    async def sql_update_action_user_restaraunt(self, id_user: int, name_menu) -> None:
        self.__cur.execute('''
                        UPDATE actions_user
                        SET name_restaurant = ?
                        WHERE id_user = ?
                    ''', (name_menu, id_user))
        self.__conn.commit()

    """Действия пользователя"""
    async def sql_action_user(self, id_user, name_restaurant, name_menu):
        try:
            self.__cur.execute('''
                                    INSERT INTO
                                    actions_user(
                                        id_user,
                                        name_restaurant,
                                        name_menu

                                    )
                                    VALUES(?, ?, ?)
                                ''', (id_user, name_restaurant, name_menu))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True


    """оБНОВЛЕНИЕ ДПННЫХ В ТАБЛИЦЕ АКТИВНОСТЬ"""
    async def sql_update_action_user(self, id_user: int,  name_menu) -> None:
        self.__cur.execute('''
                    UPDATE actions_user
                    SET name_menu = ?
                    WHERE id_user = ?
                ''', (name_menu[0], id_user))
        self.__conn.commit()

    """Получение name_restaurant пользователя в таблице АКТИВНОСТЬ"""
    async def sql_show_user_action_name_restaurant(self, user_id) -> list:
        result = f"SELECT name_restaurant FROM actions_user WHERE id_user = {user_id}"
        return self.__cur.execute(result).fetchall()

    """Получение name_menu пользователя в таблице АКТИВНОСТЬ"""
    async def sql_show_user_action_name_name_menu(self, user_id) -> list:
        result = f"SELECT name_menu FROM actions_user WHERE id_user = {user_id}"
        return self.__cur.execute(result).fetchall()



    """КОРЗИНА"""
    """Добавление товара в корзину"""
    async def sql_add_basket(self, user_name, name_product, count, price, new_price):
        try:
            self.__cur.execute('''
                                    INSERT INTO
                                    basket_user(
                                        user_id,
                                        basket,
                                        count,
                                        price,
                                        new_price

                                    )
                                    VALUES(?, ?, ?, ?, ?)
                                ''', (user_name, name_product, count, price, new_price))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Изменение состава продукта"""
    async def sql_compound(self, name_product: str):
        name = str(name_product)
        result = f"SELECT products.name, compound.name_compound, compound.count " \
                 f" FROM product_compound" \
                 f" JOIN products on products.id = product_compound.id_product" \
                 f" JOIN compound on compound.id = product_compound.id_compound" \
                 f" WHERE products.name = '{name_product}'"
        return self.__cur.execute(result).fetchall()

    """Добавление в таблицу временного пользовательского состава"""
    async def sql_user_compound(self, id_user, name_production, compound_name, count, const_count, comment):
        try:
            self.__cur.execute('''
                INSERT INTO
                user_compound(
                    user_id,
                    name_production,
                    compound_name,
                    count,
                    const_count,
                    comment
                    )
                VALUES(?, ?, ?, ?, ?, ?)
                ''', (id_user, name_production, compound_name, count, const_count, comment))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Проверка на сущкствование во временной таблице"""
    async def sql_examination_user_compound(self, id_user, name_production):
        result = f"SELECT * FROM user_compound WHERE user_id = {id_user} AND name_production = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """Обновление коментария во временной таблице"""
    async def sql_update_user_compound(self, user_id, name_production, compound_name, comment):
        result = f'UPDATE user_compound SET comment = "{comment}" WHERE user_id = "{user_id}" ' \
                 f'AND name_production = "{name_production}" AND compound_name = "{compound_name}"'
        self.__cur.execute(result)
        self.__conn.commit()

    """Обновление количества во временной таблице"""
    async def sql_update_count_user_compound(self, user_id, name_production, compound_name, count):
        result = f'UPDATE user_compound SET count = "{count}" WHERE user_id = "{user_id}" ' \
                 f'AND name_production = "{name_production}" AND compound_name = "{compound_name}"'
        self.__cur.execute(result)
        self.__conn.commit()

    """Вывод измененых данных из временной таблицы"""
    async def sql_new_user_compound(self, id_user, name_production) -> list:
        result = f"SELECT name_production, compound_name, count, const_count, comment " \
                 f" FROM user_compound " \
                 f" WHERE user_id = {id_user}" \
                 f" AND name_production = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """Вывод коментария из временной таблицы"""
    async def sql_comment_user_compound(self, id_user, name_production, compound_name) -> list:
        result = f"SELECT comment FROM user_compound WHERE user_id = {id_user}" \
                 f" AND name_production = '{name_production}' AND compound_name = {compound_name}"
        return self.__cur.execute(result).fetchall()

    """Вывод ___ из временной таблицы"""
    async def sql_user_nameProd_Com_user_compound(self, id_user) -> list:
        result = f"SELECT name_production, comment FROM user_compound WHERE user_id = {id_user} "
        return self.__cur.execute(result).fetchall()

    """Вывод ___ из временной таблицы"""
    async def sql_user_nameProd_user_compound(self, id_user, name_production) -> list:
        result = f"SELECT * FROM user_compound WHERE user_id = {id_user} " \
                 f"AND name_production = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """Обновления коментария во временной таблице"""
    async def sql_update_coment_user_compound(self, comment, user_id, name_production, compound_name):
        result = f'UPDATE user_compound SET comment = "{comment}" WHERE user_id = "{user_id}" ' \
                 f'AND name_production = "{name_production}" AND compound_name = "{compound_name}"'
        self.__cur.execute(result)
        self.__conn.commit()

    """Вывод 'количества' во временной тамблице"""
    async def sql_count_user_compound(self, id_user, name_compound, name_production) -> list:
        result = f"SELECT count FROM user_compound WHERE user_id = {id_user} AND compound_name = '{name_compound}' " \
                 f"AND name_production = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """Удаление товара при оплате"""
    async def sql_delete_basket_user(self, user_id):
        result = f"DELETE FROM basket_user WHERE user_id = ?"
        self.__cur.execute(result, (user_id, ))
        self.__conn.commit()
        return self.__cur.fetchall()

    """Удаление товара при оплате в таблице user_compaund (измененого состава)"""
    async def sql_delete_user_compound(self, user_id):
        result = f"DELETE FROM user_compound WHERE user_id = {user_id}"
        return self.__cur.execute(result).fetchall()

    """Удаление товара при оплате в таблице user_compaund (измененого состава)"""
    async def sql_delete_product_user_compound(self, user_id, name_production):
        result = f"DELETE FROM user_compound WHERE user_id = {user_id} " \
                 f"AND name_production = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """Удаление товара в корзине"""
    async def sql_delete_product_basket_user(self, user_id, name_product):
        self.__cur.execute("DELETE FROM basket_user WHERE user_id = ? AND basket = ?", (user_id, name_product))
        self.__conn.commit()
        return self.__cur.fetchall()

    """Показать карзину пользователя"""
    async def sql_show_basket(self, name_user):
        result = f"SELECT * FROM basket_user WHERE {name_user}"
        return self.__cur.execute(result).fetchall()

    """Показать карзину пользователя"""
    async def sql_show_basket_product(self, name_user, name_production):
        result = f"SELECT * FROM basket_user WHERE user_id = {name_user} AND basket = '{name_production}'"
        return self.__cur.execute(result).fetchall()

    """оБНОВЛЕНИЕ ДПННЫХ В ТАБЛИЦЕ Пользовательской корзины"""
    async def sql_update_product_basket_user(self, id_user: int, count, price, name_prod) -> None:
        self.__cur.execute('''
                        UPDATE basket_user
                        SET count = ?, new_price = ?
                        WHERE user_id = ? AND basket = ?
                    ''', (count, price, id_user, name_prod))
        self.__conn.commit()




    """ОТЗЫВЫ"""
    """Таблица добавления отзывов"""
    async def sql_add_review(self, user_id, name_user, restaurant, date,  description, status):
        """ADD NEW product"""
        try:
            self.__cur.execute('''
                INSERT INTO
                    reviews(
                        user_id,
                        name_user,
                        restaurant,
                        date,
                        description,
                        status
                    )
                VALUES(?, ?, ?, ?, ?, ?)
            ''', (user_id, name_user, restaurant, date, description, status))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    """Вывод всех отзывов"""
    async def get_all_reviews(self) -> list:
        result = f"SELECT * FROM reviews WHERE status = 'Не обработан'"
        return self.__cur.execute(result).fetchall()

    """Вывод id отзыва"""
    async def get_id_review(self) -> tuple:
        """GET ALL menu"""
        self.__cur.execute(f'''
                SELECT id
                FROM reviews
            ''')
        return tuple([id_review[0] for id_review in self.__cur.fetchall()])

    async def create_all_database(self) -> None:
        """CREATE DATABASE"""
        await self.create_roles_table()
        await self.create_users_table()
        await self.create_categories_table()
        await self.create_subcategories_table()
        await self.create_products_table()
