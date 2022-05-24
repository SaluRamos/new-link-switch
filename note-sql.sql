-- MÚLTIPLAS VARIAVEIS SÃO SEPARADAS EM ','
-- VALORES ATRIBUIDOS DEVEM SER ESCRITOS ENTRE ASPAS SIMPLES

-- INSERT INTO TABLE_NAME (COLUMNS) VALUES (COLUMNS_VALUES);
-- SELECT COLUMNS FROM TABLE_NAME WHERE TARGET_COLUMN = 'VALUE';
-- UPDATE TABLE_NAME SET COLUMN = 'NEW_VALUE' WHERE TARGET_COLUMN = 'VALUE';
-- DELETE FROM TABLE_NAME WHERE TARGET_COLUMN = 'VALUE';
-- ROLLBACK

CREATE TABLE USERS(
    USERNAME TEXT,
    PASSWORD_ TEXT,
    CONSTRAINT USERS_PK PRIMARY KEY(USERNAME)
);

CREATE TABLE A_WEAPON(
    ID INT,
    _OWNER VARCHAR(42),
    DEPLETION INT,
    RARITY INT,
    MANUFACTURER TEXT,
    MANUFACTURER_ID INT, --DEFINES CATEGORY
    STARS INT,
    SECONDARY_DAMAGE_TYPE TEXT,
    MAX_DAMAGE INT,
    MIN_DAMAGE INT,
    FIRE_RATE DECIMAL,
    MOBILITY DECIMAL, --PERCENT
    RELOAD_TIME DECIMAL,
    CLIP_SIZE INT,
    CRITICAL_CHANCE DECIMAL, --PERCENT
    CRITICAL_BONUS DECIMAL, --PERCENT
    RECOIL DECIMAL,
    REACH DECIMAL,
    PENETRATION INT,
    ZOOM DECIMAL,
    CONSTRAINT A_WEAPON_PK PRIMARY KEY(ID)
);

ALTER TABLE A_WEAPON
ADD CONSTRAINT FK_WALLET_ORDER FOREIGN KEY (_OWNER) REFERENCES A_PLAYER(WALLET); --_OWNER DEVE SER UMA ROW EM A_PLAYER ---> WALLET

ALTER TABLE A_PLAYER
ALTER COLUMN _LEVEL SET DEFAULT 1;

ALTER TABLE A_PLAYER
ALTER COLUMN _EXP SET DEFAULT 1;

ALTER TABLE A_PLAYER
ADD VIP_LEVEL TEXT DEFAULT "PLAYER";