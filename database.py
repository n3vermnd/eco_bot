import aiosqlite
import math

async def create_db():
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                balance REAL NOT NULL DEFAULT 0
            );
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS vpn (
                tg_id INTEGER,
                tarif TEXT,
                vpn_sublink TEXT,
                expiryTime TEXT
            );
        ''')
        await db.commit()
        
async def recreate_db():
    async with aiosqlite.connect('users.db') as db:
        await db.execute(f'DROP TABLE IF EXISTS users;')
        await db.execute(f'DROP TABLE IF EXISTS vpn;')
        await create_db()

async def new_user(tg_id):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT tg_id FROM users WHERE tg_id = ?', (tg_id,)) as cursor:
            row = await cursor.fetchone()
            return row is None
        
async def register_user(tg_id):
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            INSERT INTO users (tg_id, balance)
            VALUES (?, 0)
        ''', (tg_id,))
        await db.commit()
        print("LOG: database.py > Пользователь успешно ЗАРЕГИСТРИРОВАН")
        
        
async def check_devices(tg_id):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT tg_id FROM vpn WHERE tg_id = ?', (tg_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                # Действия, если запись не найдена
                print(f"Устройство с tg_id {tg_id} не найдено в таблице.")
                return False  # Устройство не найдено
            else:
                # Действия, если запись найдена
                print(f"Устройство с tg_id {tg_id} уже существует в таблице.")
                return True  # Устройство найдено
        
async def get_balance(tg_id):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT balance FROM users WHERE tg_id = ?', (tg_id,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                balance = row[0]
                return str(math.ceil(balance))
            
            
async def get_tarif(tg_id):
    async with aiosqlite.connect('users.db') as db:
        # Получаем текущий тариф
        async with db.execute('SELECT tarif FROM vpn WHERE tg_id = ?', (tg_id,)) as cursor:
            row = await cursor.fetchone()     
            if row is not None:
                tarif = row[0]
                return tarif      
            

async def price_month(tg_id):
    async with aiosqlite.connect('users.db') as db:
        # Получаем текущий тариф
        async with db.execute('SELECT tarif FROM vpn WHERE tg_id = ?', (tg_id,)) as cursor:
            row = await cursor.fetchone()
        
        # Считаем количество устройств с тарифом 'ST'
        async with db.execute('SELECT COUNT(*) FROM vpn WHERE tg_id = ? AND tarif = "st"', (tg_id,)) as st_cursor:
            st_count_row = await st_cursor.fetchone()
            st_count = st_count_row[0]

        # Считаем количество устройств с тарифом 'FT'
        async with db.execute('SELECT COUNT(*) FROM vpn WHERE tg_id = ? AND tarif = "ft"', (tg_id,)) as ft_cursor:
            ft_count_row = await ft_cursor.fetchone()
            ft_count = ft_count_row[0]

        if row is not None:
            tarif = row[0]
            if tarif is None:
                return 'Тариф не подключен.'
            else:
                st_price = 150
                ft_price = 300
                return f'Ваша абонентская плата: {st_count*st_price + ft_count*ft_price}₽/мес.\nУ вас активно {st_count + ft_count} {"устройство" if (st_count + ft_count) % 10 == 1 and (st_count + ft_count) % 100 != 11 else "устройства" if 2 <= (st_count + ft_count) % 10 <= 4 and not 11 <= (st_count + ft_count) % 100 <= 14 else "устройств"}'

async def addClient(tariff, vpn_sublink, expiryTime, tg_id):
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            INSERT INTO vpn (tg_id, tarif, vpn_sublink, expiryTime)
            VALUES (?, ?, ?, ?)
''', (tg_id, tariff, vpn_sublink, expiryTime))
        print('$$$$$$$$$$ обновлено users')
        await db.commit()