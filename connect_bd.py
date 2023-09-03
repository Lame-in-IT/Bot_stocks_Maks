import psycopg2
from config import config_wb as settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import requests
import logging
import json
import openpyxl

from get_date import get_date_7


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    return create_engine(url, pool_size=50, echo=False)


def get_engine_from_settings():  # sourcery skip: raise-specific-error
    keys = ["user", "password", "host", "port", "database"]
    if any(key not in keys for key in settings.keys()):
        raise Exception("Файл настроек не правельный")
    return get_engine(settings["user"],
                      settings["password"],
                      settings["host"],
                      settings["port"],
                      settings["database"])


def get_session():
    engine = get_engine_from_settings()
    return sessionmaker(bind=engine)() # type: ignore


def connect_bd():
    return psycopg2.connect(
        database=settings["database"],
        user=settings["user"],
        password=settings["password"],
        host=settings["host"],
        port=settings["port"],
    )
    
def read_user(data_user):
    try:
        table_df = pd.read_sql(
            f"SELECT id FROM users WHERE id = {data_user['id']}", con=get_engine_from_settings())
        user_bool = len(table_df["id"])
        if user_bool >= 1:
            updata_chapter(data_user['id'], "start")
            return "Приветствуем вас снова"
        elif user_bool == 0:
            created_user(data_user)
            return "Здравствуйте"
    except Exception as err:
        return "Произошла ошибка проверки личности"
    
def created_user(data_user):
    connection = connect_bd()
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO users(id, is_bot, first_name, username, language_code, chapter)
                          VALUES(%s, %s, %s, %s, %s, %s)""", [data_user["id"], data_user["is_bot"], data_user["first_name"], data_user["username"],
                                                          data_user["language_code"], "start"])

def created_user_api(id_user, api_user):
    try:
        table_df = pd.read_sql(
            f"SELECT id FROM api_users WHERE id = {id_user}", con=get_engine_from_settings())
        user_bool = len(table_df["id"])
        if user_bool >= 1:
            updata_api_user(id_user, api_user)
            return "Да"
        elif user_bool == 0:
            up_data_approval(id_user)
            connection = connect_bd()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO api_users(id, statistic_api)
                                VALUES(%s, %s)""", [id_user, api_user])
            return "Да"
    except Exception as ex:
        logging.exception(ex)
        return "Нет"

def up_data_approval(id_user):
    try:
        connection = connect_bd()
        cursor = connection.cursor()
        sql_update_query = """Update users set approval = %s where id = %s"""
        cursor.execute(sql_update_query, ("Согласен", id_user))
        connection.commit()
    except Exception as ex:
        logging.exception(ex)
        
def updata_chapter(id_user, appeal_True):
    try:
        connection = connect_bd()
        cursor = connection.cursor()
        sql_update_query = """Update users set chapter = %s where id = %s"""
        cursor.execute(sql_update_query, (appeal_True, id_user))
        connection.commit()
    except Exception as ex:
        logging.exception(ex)

def updata_api_user(id_user, api_user):
    try:
        connection = connect_bd()
        cursor = connection.cursor()
        sql_update_query = """Update api_users set statistic_api = %s where id = %s"""
        cursor.execute(sql_update_query, (api_user, id_user))
        connection.commit()
    except Exception as ex:
        logging.exception(ex)
        
def get_chapter_user(id_user):
    try:
        table_df = pd.read_sql(
            f"SELECT * FROM users WHERE id = {id_user}", con=get_engine_from_settings())
        return table_df["chapter"][0]
    except Exception as ex:
        logging.exception(ex)
        
def get_api_wb(wb_stst_user):
    try:
        return requests.get(url=f"https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={get_date_7()}",
                            headers={'Content-Type': 'application/json', 'Authorization': f'{wb_stst_user}'}).status_code
    except Exception as ex:
        logging.exception(ex)
        return 1000

def get_id_and_api_user():
    try:
        table_user = pd.read_sql("SELECT * FROM users WHERE approval = 'Согласен'", con=get_engine_from_settings())
        list_name_user = list(table_user["first_name"])
        list_id_user = list(table_user["id"])
        list_api = []
        for item_api in list_id_user:
            table_api_user = pd.read_sql(f"SELECT * FROM api_users WHERE id = {item_api}", con=get_engine_from_settings())
            list_api.append(table_api_user['statistic_api'][0])
        return [list_name_user, list_id_user, list_api]
    except Exception as ex:
        logging.exception(ex)

def get_satat_wb():
    try:
        data_user = get_id_and_api_user()
        for index, item_api in enumerate(data_user[2]):
            full_list_contact = []
            table_wb_cards = pd.read_sql(
                    f"SELECT * FROM no_sales_for_7 WHERE stocks_user > 0 AND (sales_user = 0 AND api_user = '{item_api}')", con=get_engine_from_settings())
            contact_user = pd.read_sql(f"SELECT contacts FROM users WHERE id = {data_user[1][index]} AND approval = 'Согласен'", con=get_engine_from_settings())
            list_con = contact_user["contacts"][0].split(',')
            full_list_contact.extend(
                list_con[it_con] for it_con in range(len(list_con) - 1)
            )
            full_list_contact.append(data_user[1][index])
            return [list(table_wb_cards["nmid"]), list(table_wb_cards["supplierarticle"]), list(table_wb_cards["subject"]),
                    list(table_wb_cards["stocks_user"]), list(table_wb_cards["sales_user"]), list(table_wb_cards["link_site"]),
                    full_list_contact]
    except Exception as ex:
        logging.exception(ex)

def created_xlsx_user():
    try:
        table_user = pd.read_sql("SELECT * FROM users WHERE approval = 'Согласен'", con=get_engine_from_settings())
        contact_user = list(table_user["contacts"])
        list_name_user = list(table_user["first_name"])
        list_id_user = list(table_user["id"])
        list_api = []
        list_files = []
        full_list_con = []
        for item_api in list_id_user:
            full_list_contact = []
            table_api_user = pd.read_sql(f"SELECT * FROM api_users WHERE id = {item_api}", con=get_engine_from_settings())
            list_api.append(table_api_user['statistic_api'][0])
        for index_data_user, item_data_user in enumerate(list_api):
            contact_user = pd.read_sql(f"SELECT contacts FROM users WHERE id = {list_id_user[index_data_user]} AND approval = 'Согласен'", con=get_engine_from_settings())
            list_con = contact_user["contacts"][0].split(',')
            full_list_contact.extend(
                list_con[it_con] for it_con in range(len(list_con) - 1)
            )
            full_list_contact.append(list_id_user[index_data_user])
            full_list_con.append(full_list_contact)
            list_warehouse = []
            table_wb_cards = pd.read_sql(
                f"SELECT warehousename FROM add_leftovers_wb_user WHERE add_stocks_for_warehouse_in_7 <= -1 AND api_user = '{item_data_user}'", con=get_engine_from_settings())
            book = openpyxl.Workbook()
            del book['Sheet']
            for it_warehouse in list(table_wb_cards["warehousename"]):
                if it_warehouse not in list_warehouse:
                    list_warehouse.append(it_warehouse)
                    sheet = book.create_sheet(it_warehouse.strip())
                    sheet["A1"] = "Артикул"
                    sheet.column_dimensions['A'].width = 30
                    sheet["B1"] = "Название"
                    sheet.column_dimensions['B'].width = 30
                    sheet["C1"] = "Размер"
                    sheet.column_dimensions['C'].width = 30
                    sheet["D1"] = "Остатки на складе"
                    sheet.column_dimensions['D'].width = 30
                    sheet["E1"] = "Продажи со склада"
                    sheet.column_dimensions['E'].width = 30
                    sheet["F1"] = "Поставки на 2 недели"
                    sheet.column_dimensions['F'].width = 30
                    table_wb_warehouse = pd.read_sql(
                        f"SELECT * FROM add_leftovers_wb_user WHERE add_stocks_for_warehouse_in_7 <= -1 AND (api_user = '{item_data_user}' AND warehousename = '{it_warehouse}')", con=get_engine_from_settings())
                    for index_create_data, item_create_data in enumerate(list(table_wb_warehouse["supplierarticle"])):
                        index_sheet = index_create_data + 2
                        sheet[f"A{index_sheet}"] = item_create_data
                        sheet[f"B{index_sheet}"] = table_wb_warehouse["subject"][index_create_data]
                        sheet[f"C{index_sheet}"] = table_wb_warehouse["techsize"][index_create_data]
                        sheet[f"D{index_sheet}"] = table_wb_warehouse["stocks_in_warehouse"][index_create_data]
                        sheet[f"E{index_sheet}"] = table_wb_warehouse["sales_in_week"][index_create_data]
                        sheet[f"F{index_sheet}"] = (table_wb_warehouse["add_stocks_for_warehouse_in_7"][index_create_data] * -1) * 2
            book.save(f"Нехватка товара на складах для {list_name_user[index_data_user]} (id {list_id_user[index_data_user]}).xlsx")
            book.close()
            list_files.append(f"Нехватка товара на складах для {list_name_user[index_data_user]} (id {list_id_user[index_data_user]}).xlsx")
        return [full_list_con, list_files]
    except Exception as ex:
        logging.exception(ex)

def create_comtact(id_user, contact):
    # sourcery skip: use-fstring-for-concatenation
    try:
        str_id_cont = str(contact)
        table_contact = pd.read_sql(
            f"SELECT contacts FROM users WHERE id = {id_user} AND approval = 'Согласен'", con=get_engine_from_settings())
        contact_str = table_contact["contacts"][0]
        connection = connect_bd()
        cursor = connection.cursor()
        sql_update_query = """Update users set contacts = %s where id = %s"""
        if contact_str is None:
            cursor.execute(sql_update_query, (str_id_cont + ',', id_user))
        else:
            list_contact = contact_str.split(",")
            if str_id_cont in list_contact:
                return f"Контакт {str_id_cont} у вас уже есть"
            cursor.execute(sql_update_query, (contact_str + str_id_cont + ',', id_user))
        connection.commit()
        return f"Контакт {str_id_cont} добавлен в ваши контакты"
    except Exception as ex:
        logging.exception(ex)

if __name__=="__main__":
    get_satat_wb()
    