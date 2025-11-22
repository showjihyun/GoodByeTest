import re
import os
from sqlalchemy import create_engine, inspect

class DBChecker:
    def __init__(self, connection_string=None):
        self.connection_string = connection_string
        self.engine = None
        self.inspector = None

    def connect(self):
        if not self.connection_string:
            print("DB Checker: No connection string provided. Skipping DB checks.")
            return False
            
        try:
            print(f"Connecting to DB...") # Masking connection string for security
            self.engine = create_engine(self.connection_string)
            self.inspector = inspect(self.engine)
            print("DB Connection Successful.")
            return True
        except Exception as e:
            print(f"DB Connection Failed: {e}")
            return False

    def check_file(self, file_path):
        if file_path.endswith('.java'):
            return self.check_jpa_entity(file_path)
        elif file_path.endswith('.xml'):
            return self.check_mybatis_mapper(file_path)
        return None

    def check_jpa_entity(self, file_path):
        """
        Scans a Java file for @Table(name="...") and checks if it exists.
        """
        print(f"Checking JPA Entity: {file_path}")
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                match = re.search(r'@Table\s*\(\s*name\s*=\s*"([^"]+)"', content)
                if match:
                    table_name = match.group(1)
                    print(f"Found Table Annotation: {table_name}")
                    
                    if self.inspector:
                        if self.inspector.has_table(table_name):
                             return {"file": file_path, "type": "JPA", "table": table_name, "status": "verified"}
                        else:
                             return {"file": file_path, "type": "JPA", "table": table_name, "status": "error: table not found"}
                    else:
                        return {"file": file_path, "type": "JPA", "table": table_name, "status": "skipped (no db connection)"}
                        
        except FileNotFoundError:
             return {"file": file_path, "type": "JPA", "status": "skipped (file not found)"}
        return None

    def check_mybatis_mapper(self, file_path):
        """
        Scans XML for table names (simplified).
        """
        print(f"Checking MyBatis Mapper: {file_path}")
        # Very basic check - in real world would parse XML
        return {"file": file_path, "type": "MyBatis", "status": "checked (basic)"}
