from __future__ import annotations

from app.config import get_config


def _import_pyodbc():
    """Lazy import pyodbc to allow app startup without ODBC driver installed."""
    import pyodbc

    return pyodbc


def get_connection_string() -> str | None:
    """Build ODBC connection string from saved config."""
    config = get_config()
    if not config:
        return None
    return (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']};"
        "TrustServerCertificate=yes;"
    )


def get_connection():
    """Create a database connection."""
    pyodbc = _import_pyodbc()
    conn_str = get_connection_string()
    if not conn_str:
        return None
    return pyodbc.connect(conn_str, timeout=10)


def test_connection(server: str, username: str, password: str) -> tuple[bool, str]:
    """Test database connection with given credentials."""
    try:
        pyodbc = _import_pyodbc()
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE=hospimag;"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str, timeout=10)
        conn.close()
        return True, "تم الاتصال بنجاح"
    except Exception as e:
        return False, f"فشل الاتصال: {e}"


def get_waiting_patients() -> list[dict]:
    """Fetch patients who are waiting (Drentertime is NULL)."""
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT Tktno, Pname, Drname, Countertime, Status, Usr, Dt
            FROM dbo.Tktno
            WHERE Drentertime IS NULL
              AND Dt = CAST(GETDATE() AS DATE)
            ORDER BY Countertime ASC
            """
        )
        columns = [col[0] for col in cursor.description]
        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, col in enumerate(columns):
                val = row[i]
                if val is not None and hasattr(val, "isoformat"):
                    val = val.isoformat()
                row_dict[col] = val if val is not None else ""
            rows.append(row_dict)
        return rows
    finally:
        conn.close()


def confirm_patient_entry(tktno: str) -> tuple[bool, str]:
    """Mark a patient as entered to the doctor by setting Drentertime."""
    conn = get_connection()
    if not conn:
        return False, "لا يوجد اتصال بقاعدة البيانات"
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE dbo.Tktno
            SET Drentertime = GETDATE(), Status = N'دخل'
            WHERE Tktno = ? AND Drentertime IS NULL
            """,
            (tktno,),
        )
        conn.commit()
        if cursor.rowcount > 0:
            return True, "تم تأكيد دخول المريض"
        return False, "لم يتم العثور على المريض أو تم تأكيد دخوله مسبقاً"
    except Exception as e:
        return False, f"حدث خطأ: {e}"
    finally:
        conn.close()
