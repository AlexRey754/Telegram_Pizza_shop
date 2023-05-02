from utils.db_api.db import add_position_to_db, delete_products_for_test

products = [
   {
        'name' : 'Піца Канзас',
        'category': 'Піца',
        'description': 'Соус Барбекю, Моцарела, Цибуля, Ковбаски баварські, Кукурудза, Гриби',
        'img_name': 'kanzas.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Пепероні',
        'category': 'Піца',
        'description': 'Соус Барбекю, Моцарела, Помідори, Пепероні',
        'img_name': 'peperoni.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Манхеттен',
        'category': 'Піца',
        'description': 'Моцарела, Пепероні, Соус Альфредо, Гриби',
        'img_name': 'manhetten.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Шинка Та Гриби',
        'category': 'Піца',
        'description': 'Моцарела, Соус(майонез+кетчуп), Гриби, Шинка',
        'img_name': 'meatandmushrooms.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Гриль',
        'category': 'Піца',
        'description': 'Болгарський перець, Курка, Соус Барбекю, Моцарела, Цибуля, Фрикадельки, Бекон',
        'img_name': 'barbeque.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Маргарита',
        'category': 'Піца',
        'description': 'Моцарела(x2), Соус',
        'img_name': 'margarita.jpg',
        'price': 231
    },
    {
        'name' : 'Піца Карбонара',
        'category': 'Піца',
        'description': 'Моцарела, Соус, Цибуля, Гриби, Шинка, Бекон',
        'img_name': 'karbonara.jpg',
        'price': 231
    },
    {
        'name' : 'Напій BonAqua Газована 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'bonaqua.jpg',
        'price': 38
    },
    {
        'name' : 'Напій Coca-Cola Zero 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'colazero.jpg',
        'price': 41
    },
    {
        'name' : 'Напій Fanta Апельсин 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'fanta.jpg',
        'price': 41
    },
    {
        'name' : 'Напій Sprite 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'sprite.jpg',
        'price': 41
    },
    {
        'name' : 'Напій Fuzetea 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'fuzetea.jpg',
        'price': 55
    },
    {
        'name' : 'Напій Schweppes Мохіто 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'schweppesmohito.jpg',
        'price': 55
    },
    {
        'name' : 'Напій Schweppes Індіан Тонік 0,5л',
        'category': 'Напій',
        'description': '',
        'img_name': 'schweppesindian.jpg',
        'price': 55
    },
    {
        'name' : 'Десерт Сіннамон Роли',
        'category': 'Десерт',
        'description': '4шт Сінамона',
        'img_name': 'sinamon.jpg',
        'price': 110
    },
    {
        'name' : 'Десерт Тірамісу',
        'category': 'Десерт',
        'description': '300 г',
        'img_name': 'tiramisu.jpg',
        'price': 110
    },
    {
        'name' : 'Десерт Шоколадний фондан',
        'category': 'Десерт',
        'description': '97 г',
        'img_name': 'fondan.jpg',
        'price': 110
    },
    {
        'name' : 'Десерт Лава Кейк',
        'category': 'Десерт',
        'description': '96 г',
        'img_name': 'lavacake.jpg',
        'price': 90
    },
    {
        'name' : 'Десерт Мафін Кокосовий',
        'category': 'Десерт',
        'description': '80 г',
        'img_name': 'mafincocoanut.jpg',
        'price': 90
    },  
    
]

def upload_all(reload=True):
    if reload:
        delete_products_for_test()
        for product in products:
            add_position_to_db(product)
        print('Reload [ON]')

    else:
        print('Reload [OFF]')
        return