import sqlite3
import pandas as pd
from typing import Dict, Any

class FinancialDatabase:
    def __init__(self, db_path="financials.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Initialize the SQLite database schema.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table to store basic extracted metrics
        # We store them as a single row for the current IPO
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT UNIQUE,
                value REAL,
                unit TEXT DEFAULT 'Crores',
                period TEXT DEFAULT 'Latest Year'
            )
        ''')
        
        conn.commit()
        conn.close()

    def store_metrics(self, metrics: Dict[str, Any]):
        """
        Stores the extracted dictionary of metrics into the DB.
        metrics: {'revenue': 100.5, 'pat': 10.2, ...}
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for key, value in metrics.items():
            if value is not None:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO financials (metric_name, value)
                        VALUES (?, ?)
                    ''', (key, value))
                except sqlite3.Error as e:
                    print(f"⚠️ DB Error inserting {key}: {e}")

        conn.commit()
        conn.close()
        print(f"✅ Stored {len(metrics)} financial metrics in SQLite.")

    def get_metric(self, metric_name: str) -> float:
        """
        Retrieve a specific metric value.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM financials WHERE metric_name = ?", (metric_name,))
        row = cursor.fetchone()
        
        conn.close()
        return row[0] if row else None

    def get_all_metrics(self) -> Dict[str, float]:
        """
        Retrieve all metrics as a dictionary.
        """
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT metric_name, value FROM financials", conn)
        conn.close()
        
        return dict(zip(df.metric_name, df.value))

if __name__ == "__main__":
    # Test stub
    pass
