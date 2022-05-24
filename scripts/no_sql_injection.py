from scripts.general import General

class NoSqlInjection:

    def verify_message(messages):
        for i in messages:
            try:
                message = i.upper()
                filter_chars = ["'", "|", "<", ">", "!", "*", '"', "(", ")", "[", "]", "{", "}", " "]
                filter_words = ["SELECT", "ALTER", "TABLE", "CREATE", "DATABASE", "ADD", "DROP", "COLUMN", "SET", "DEFAULT ", "NULL", "CONSTRAINT", "FOREIGN", "REFERENCES", "BACKUP", "CHECK", "INDEX", "WHERE", "UPDATE"]
                for i in filter_chars:
                    if i in message:
                        raise Exception(f"char '{i}' (ascii = {ord(i)}) not allowed")
                for i in filter_words:
                    if i in message:
                        raise Exception(f"word '{i}' not allowed")
            except Exception as e:
                General.error(str(e))
                return False
        return True