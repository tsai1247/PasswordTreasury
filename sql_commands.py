class sql_commands:
    TREASURY_CREATE = '''
        CREATE TABLE "treasury" (
            "ID"	INTEGER NOT NULL UNIQUE,
            "Platform"	INTEGER NOT NULL,
            "Account"	TEXT NOT NULL,
            "Password"	INTEGER NOT NULL,
            "Remark"	INTEGER,
            "ModifyDate"	INTEGER NOT NULL,
            "CreateDate"	INTEGER NOT NULL,
            PRIMARY KEY("ID" AUTOINCREMENT)
        );
    '''

    TREASURY_SEARCH = '''
        SELECT Platform, Account, Password, Remark FROM treasury
        WHERE 1=1 [CONDITION]
    '''

    TREASURY_INSERT = '''
        INSERT INTO treasury (Platform, Account, Password, Remark, ModifyDate, CreateDate)
        VALUES(?, ?, ?, ?, ?, ?)
    '''
    
    TREASURY_DELETE = '''
        DELETE FROM treasury
        WHERE 1=1 [CONDITION]
    '''

    TREASURY_UPDATE = '''
        UPDATE treasury
        SET 
    '''

    TREASURY_TABLE_CHECK = '''
        SELECT name FROM sqlite_master WHERE type='table' AND name='treasury'
    '''