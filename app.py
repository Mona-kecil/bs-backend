from dotenv import load_dotenv
import os
from fastapi import FastAPI
from supabase import create_client, Client

# Buat ambil URL dan API key dari .env
load_dotenv()
URL = os.getenv("LINK_URL")
KEY = os.getenv("API_KEY")

# Membuat client Supabase dan bikin API
supabase: Client = create_client(URL, KEY)
app = FastAPI()


# Panggilan function untuk fetch data dari API nya
@app.get("/api/v1/vehicles") # Buat tampilin semua data tabel kendaraan
async def get_vehicles():
    response = supabase.table("vehicles").select("*").execute()
    return response.data

@app.get("/api/v1/vehicles/{license_plate}") # Buat tampilin semua data tabel kendaraan berdasarkan plat kendaraan
async def get_vehicle_by_license_plate(license_plate: str):
    response = supabase.table("vehicles").select("*").eq("license_plate", license_plate).execute()
    return response.data

@app.get("/api/v1/transactions") # Buat tampilin semua data tabel transaksi
async def get_transactions():
    response = supabase.table("transactions").select("*").execute()
    return response.data

@app.get("/api/v1/transactions/{id}") # Buat tampilin semua data tabel transaksi berdasarkan ID nya
async def get_transaction_by_id(id: str):
    response = supabase.table("transactions").select("*").eq("id", id).execute()
    return response.data

@app.post("/api/v1/transactions") # Buat jejak transaksi kendaraan baru
async def create_transaction(transaction: dict):
    response = supabase.table("transactions").insert(transaction).execute()
    return response.data

@app.patch("/api/v1/transactions/{id}") # Buat update transaksi spesifik berdasarkan ID
async def update_transaction(id: str, transaction: dict):
    """Update a specific transaction record by its ID."""
    response = supabase.table("transactions").update(transaction).eq("id", id).execute()
    return response.data

@app.get("/api/v1/overdue-payments") # Buat tampilin semua transaksi yang sudah dibayar tetapi belum keluar dalam waktu 15 menit
async def get_overdue_payments():
    response = supabase.table("transactions").select("*").eq("payment_status", "paid").is_("exit_time", None).execute()
    return response.data

@app.get("/api/v1/dashboard") # Buat tampilin data dashboard
async def get_dashboard():
    vehicles_count = supabase.table("vehicles").select("count", count="exact").execute()
    transactions_count = supabase.table("transactions").select("count", count="exact").execute()
    overdue_count = supabase.table("transactions").select("count", count="exact").eq("payment_status", "paid").is_("exit_time", None).execute()

    return {
        "total_vehicles": vehicles_count["count"],
        "total_transactions": transactions_count["count"],
        "overdue_transactions": overdue_count["count"]
    }

@app.post("/api/v1/manual-actions") # Endpoint untuk para Admin melakukan aksi manualnya
async def manual_actions(action: dict):
    response = supabase.table("logs").insert(action).execute()
    return response.data
