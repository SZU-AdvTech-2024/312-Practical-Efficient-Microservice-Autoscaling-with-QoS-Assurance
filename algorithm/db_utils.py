import sqlite3
import time


class QValueDB:
    def __init__(self):
        self.connection = self.create_connecction()
        self.create_table()

    def create_connecction(self):
        try:
            self.connection = sqlite3.connect("databases/q_value_table.db")
            return self.connection
        except sqlite3.Error as e:
            print(e)
        return None

    def create_table(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS q_values(
        slo NOT NULL,
        range_id NOT NULL,
        q_value NOT NULL);
        '''
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def get_q_value(self, slo, range_id):
        query = '''SELECT * FROM q_values WHERE slo=? AND range_id=?'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        return rows

    def save_q_value(self, slo, range_id, q_value):
        insert_sql = '''INSERT INTO q_values(slo, range_id, q_value) VALUES (?,?,?)'''
        if self.connection:
            c = self.connection.cursor()
            c.execute(insert_sql, (slo, range_id, q_value))
            self.connection.commit()
        else:
            print("Connection Error")

    def close_connection(self):
        self.connection.close()

    def get_data(self, query=None):
        get_data_sql = '''SELECT * FROM q_values;'''
        c = self.connection.cursor()
        c.execute(get_data_sql)
        rows = c.fetchall()
        for row in rows:
            print(row)

    def delete_table(self):
        """清空历史记录表"""
        try:
            query = '''DELETE FROM q_values WHERE slo=250'''
            c = self.connection.cursor()
            c.execute(query)
            self.connection.commit()
            print("Table 'q_values' has been cleared.")
        except sqlite3.Error as e:
            print(f"Error while clearing table: {e}")



class HistoryDB:
    def __init__(self):
        self.db_file = "databases/experiment_history.db"
        self.connection = self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            return self.connection
        except sqlite3.Error as e:
            print(e)
        return None

    def create_table(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY,
        experiment_id INTEGER,
        experiment_time TEXT NOT NULL,
        range_id INTEGER NOT NULL ,
        rps_range TEXT NOT NULL ,
        rps REAL NOT NULL ,
        slo REAL NOT NULL ,
        response REAL ,
        cost REAL NOT NULL ,
        delta_si REAL,
        delta_response REAL,
        n_s INT,
        current_configs TEXT NOT NULL ,
        metrics TEXT NOT NULL,
        next_configs TEXT NOT NULL, 
        threshold REAL,
        container_stats TEXT,
        early_slo_violation REAL,
        detection_time REAL,
        responses TEXT);
        '''
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)

    def close_connection(self):
        self.connection.close()

    def clear_table(self):
        """清空历史记录表"""
        try:
            query = '''DELETE FROM history'''
            c = self.connection.cursor()
            c.execute(query)
            self.connection.commit()
            print("Table 'history' has been cleared.")
        except sqlite3.Error as e:
            print(f"Error while clearing table: {e}")

    def delete_table(self):
        """清空历史记录表"""
        try:
            query = '''DELETE FROM history WHERE range_id=3'''
            c = self.connection.cursor()
            c.execute(query)
            self.connection.commit()
            print("Table 'history' has been cleared.")
        except sqlite3.Error as e:
            print(f"Error while clearing table: {e}")

    def select_cost_min(self, slo, range_id):
        query = '''SELECT * FROM history WHERE slo=? AND range_id=? And early_slo_violation=0 ORDER BY cost ASC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        # c.execute(query, (range_id,))
        rows = c.fetchall()
        return rows

    def insert_into_table(self, data):
        last_row_id = 0
        insert_value_sql = '''INSERT INTO history(experiment_id, experiment_time, range_id, rps_range, rps, slo, response, cost, delta_si,
        delta_response, n_s, current_configs, metrics, next_configs, threshold, container_stats, early_slo_violation, detection_time, responses) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        if self.connection:
            try:
                c = self.connection.cursor()
                c.execute(insert_value_sql, (
                    data["experiment_id"], data["time"], data["range_id"], str(data["rps_range"]), data["rps"],
                    data["slo"], data["response"], data["cost"], data["delta_si"], data["delta_response"],
                    data["n_s"], str(data["current_configs"]), str(data["metrics"]),str(data["next_configs"]),
                    data["threshold"], str(data["container_stats"]), data['early_slo_violation'], data['detection_time'], str(data['responses'])))
                last_row_id = c.lastrowid
                self.connection.commit()
            except sqlite3.Error as e:
                print("Insertion failed")
                print(e)
        else:
            print("Connection Error")
        return last_row_id

    def get_data(self, query=None):
        get_data_sql = '''SELECT * FROM history;'''
        c = self.connection.cursor()
        c.execute(get_data_sql)
        rows = c.fetchall()
        for row in rows:
            print(row)


    def select_response_regression(self, slo, range_id):
        query = '''SELECT * FROM history WHERE slo=? AND range_id=?'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        # c.execute(query, (range_id,))
        rows = c.fetchall()
        return rows

    def get_configuration_with_higher_cost(self, slo, range_id, cost):
        query = '''SELECT * FROM history WHERE delta_response>0 AND cost>? AND slo=? AND range_id=? ORDER BY id DESC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (cost, slo, range_id))
        rows = c.fetchall()

        if rows:
            data = rows[0]
            current_settings = {"id": data[0], "experiment_id": data[1], "experiment_time": data[2], "range_id": data[3],
                                "rps_range": data[4], "rps": data[5], "slo": data[6], "response": data[7], "cost": data[8],
                                "delta_si": data[9], "delta_response": data[10], "n_s": data[11], "current_configs": data[12],
                                "metrics": data[13], "next_configs": data[14], "threshold": data[15], "container_stats": data[16],
                                'early_slo_violation': data[17], "detection_time": data[18], "responses": data[19]}
            return current_settings
        return None

    def get_last_configuration(self, slo, range_id):
        query = '''SELECT * FROM history WHERE slo=? AND range_id=? ORDER BY id DESC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        if rows:
            data = rows[0]
            current_settings = {"id": data[0], "experiment_id": data[1], "experiment_time": data[2], "range_id": data[3],
                                "rps_range": data[4], "rps": data[5], "slo": data[6], "response": data[7], "cost": data[8],
                                "delta_si": data[9], "delta_response": data[10], "n_s": data[11], "current_configs": data[12],
                                "metrics": data[13], "next_configs": data[14], "threshold": data[15], "container_stats": data[16],
                                "early_slo_violation":data[17], "detection_time": data[18], "responses": data[19]}
            return current_settings
        return None

    def get_last_inserted_id(self, slo, range_id):
        query = '''SELECT id FROM history WHERE slo=? AND range_id=? ORDER BY id DESC LIMIT 1'''
        c = self.connection.cursor()
        c.execute(query, (slo, range_id))
        rows = c.fetchall()
        return rows

    def update_latency_of_last_config(self, config_id, latency):
        query = '''UPDATE history SET response=? WHERE id=?'''
        if self.connection:
            try:
                c = self.connection.cursor()
                c.execute(query, (latency, config_id))
                self.connection.commit()
            except sqlite3.Error as e:
                print(e)
        else:
            print('Connection Error')
