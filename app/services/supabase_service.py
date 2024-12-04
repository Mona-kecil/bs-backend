import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv("SUPABASE_URL")
API_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(URL, API_KEY)


def fetch_table_data(table_name: str, filters: dict = None):
    """
    Fetch data from mentioned table

    @param table_name: Name of the table
    @param filters: Filters to be applied on the table

    @return: Data from the table
    """
    query = supabase.table(table_name).select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    return query.execute()


def insert_data(table_name: str, data: dict):
    """
    Insert data into the table

    @param table_name: Name of the table
    @param data: Data to be inserted

    @return: Newly inserted data
    """
    return supabase.table(table_name).insert(data).execute()


def update_data(table_name: str, data: dict, filters: dict):
    """
    Update data in the table

    @param table_name: Name of the table
    @param data: Data to be updated
    @param filters: Filters to be applied on the table

    @return: Updated data
    """
    query = supabase.table(table_name).update(data)
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    return query.execute()


def delete_data(table_name: str, filters: dict):
    """
    Delete data from the table

    @param table_name: Name of the table
    @param filters: Filters to be applied on the table

    @return: Deleted data
    """
    query = supabase.table(table_name).delete()
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    return query.execute()
