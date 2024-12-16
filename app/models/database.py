import sqlite3

DB_PATH = 'app/data/database.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_sessions (
            id UUID PRIMARY KEY,
            license_plate VARCHAR NOT NULL,
            entry_time TIMESTAMP NOT NULL,
            exit_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP DEFAULT NULL
        )
        """)

        cursor.execute("""
        CREATE UNIQUE INDEX unique_license_plate_active
        ON parking_sessions (license_plate)
        WHERE deleted_at IS NULL
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id UUID PRIMARY KEY,
            parking_session_id UUID NOT NULL REFERENCES parking_sessions(id),
            payment_method VARCHAR NOT NULL DEFAULT 'none',
            amount INTEGER NOT NULL,
            payment_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP DEFAULT NULL
        )
        """)

        cursor.execute("""
        CREATE TRIGGER enforce_payment_before_exit
        BEFORE UPDATE ON parking_sessions
        WHEN NEW.exit_time IS NOT NULL OR NEW.deleted_at IS NOT NULL
        BEGIN
            SELECT CASE
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM payments
                    WHERE payments.parking_session_id = NEW.id
                )
                THEN RAISE(FAIL, 'Cannot close session: No payment found')
            END;
        END;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id UUID PRIMARY KEY,
            related_id UUID,
            related_table VARCHAR NOT NULL,
            action VARCHAR NOT NULL,
            notes TEXT,
            created_by VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted_at TIMESTAMP DEFAULT NULL
        )
        """)

        conn.commit()


if __name__ == "__main__":
    init_db()
