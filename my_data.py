from sqlalchemy import MetaData, Table, Column, SmallInteger, String, Float, PrimaryKeyConstraint

# MySQL database details
db_conn_config = {
    'user': 'Giulio',
    'password': 'Capuozz0123!',
    'host': 'localhost',
    'database': 'dgt_database'
}

# Suppliers list
suppliers_list = {
    'WHEEL PROS': 'WP',
}

# database metadata
db_metadata = MetaData()
master_stock_list = Table(
    "master_stock_list",
    db_metadata,
    Column('SKU CODE (UNIQUE)', String(50), nullable=False),
    Column('ITEM CODE', String(200)),
    Column('IMAGE SKU 1', String(50)),
    Column('IMAGE SKU 2', String(50)),
    Column('IMAGE SKU 3', String(50)),
    Column('IMAGE SKU 4', String(50)),
    Column('IMAGE SKU 5', String(50)),
    Column('IMAGE SOURCE', String(50)),
    Column('IMAGE 1 URL', String(500)),
    Column('IMAGE 2 URL', String(500)),
    Column('IMAGE 3 URL', String(500)),
    Column('IMAGE 4 URL', String(500)),
    Column('IMAGE 5 URL', String(500)),
    Column('VIDEO 1 URL', String(500)),
    Column('STOCK STATUS', String(50)),
    Column('CONSTRUCTION TYPE', String(50)),
    Column('MATERIAL', String(50)),
    Column('SUPPLIER LOCATION', String(50)),
    Column('WHEEL OWNER', String(50), nullable=False),
    Column('BRAND', String(50)),
    Column('BRAND LOGO', String(500)),
    Column('WHEEL MODEL', String(50)),
    Column('SIZE', String(50)),
    Column('J WIDTH', String(50)),
    Column('SIZE DESC', String(50)),
    Column('PCD', String(50)),
    Column('MIN BOLT (IF BLANK)', SmallInteger),
    Column('MAX BOLT (IF BLANK)', SmallInteger),
    Column('MIN LUG (IF BLANK)', SmallInteger),
    Column('MAX LUG (IF BLANK)', SmallInteger),
    Column('ET', String(50)),
    Column('MIN ET', String(50)),
    Column('MAX ET', String(50)),
    Column('CB', Float),
    Column('COLOUR', String(50)),
    Column('FINISH', String(50)),
    Column('WEIGHT LOAD (KG)', Float),
    Column('WHEEL WEIGHT (KG)', Float),
    Column('BOLT SEATING', SmallInteger),
    Column('STAGGERED CODE', String(50)),
    Column('STAGGERED OPTION', String(50)),
    Column('STAGG UNIQUE SKU LOOKUP', String(50)),
    Column('STAGGERED POSITION', String(50)),
    Column('STAGGERED FRONT FILTER', String(50)),
    Column('QUANTITY (SETS AVAILABLE)', SmallInteger),
    Column('SHIPPING WEIGHT', SmallInteger),
    Column('SHIPPING (DOMESTIC)', Float),
    Column('SHIPPING (INTERNATIONAL)', Float),
    Column('MSRP', Float),
    Column('PRICE MARK UP', Float),
    Column('TOTAL UNIQUE PRICE (MSRP + MARGIN)', Float),
    Column('B STOCK IDENTIFIER', String(50)),
    Column('DISCOUNTED PRICE', Float),
    Column('SINGLE OR SET FILTER', String(50)),
    Column('IMPORT / DISPLAY FILTER', String(50)),
    Column('BRAND LOGO_[0]', String(500)),
    Column('BRAND BANNER', String(500)),
    Column('BRAND VIDEO 1', String(500)),
    Column('BRAND VIDEO 2', String(500)),
    Column('WHEEL DESCRIPTION', String(500)),
    Column('SEO KEYWORDS', String(500)),
    Column('GROUP IDENTIFIER', String(500)),
    PrimaryKeyConstraint('SKU CODE (UNIQUE)', 'WHEEL OWNER')
)



# using MSQAlchemy ORM to build table
# class Master_stock_list(Base):
#     __tablename__ = 'master_stock_list'
#
#     'SKU CODE (UNIQUE)' = Column(String(50), primary_key=True, nullable=False)
#     'ITEM CODE' = Column(String(200))
#     'IMAGE SKU 1' = Column(String(50))
#     'IMAGE SKU 2' = Column(String(50))
#     'IMAGE SKU 3' = Column(String(50))
#     'IMAGE SKU 4' = Column(String(50))
#     'IMAGE SKU 5' = Column(String(50))
#     'IMAGE SOURCE' = Column(String(50))
#     'IMAGE 1 URL' = Column(String(500))
#     'IMAGE 2 URL' = Column(String(500))
#     'IMAGE 3 URL' = Column(String(500))
#     'IMAGE 4 URL' = Column(String(500))
#     'IMAGE 5 URL' = Column(String(500))
#     'VIDEO 1 URL' = Column(String(500))
#     'STOCK STATUS' = Column(String(50))
#     'CONSTRUCTION TYPE' = Column(String(50))
#     'MATERIAL' = Column(String(50))
#     'SUPPLIER LOCATION' = Column(String(50))
#     'WHEEL OWNER' = Column(String(50), nullable=False)
#     'BRAND' = Column(String(50))
#     'BRAND LOGO' = Column(String(500))
#     'WHEEL MODEL' = Column(String(50))
#     'SIZE' = Column(String(50))
#     'J WIDTH' = Column(String(50))
#     'SIZE DESC' = Column(String(50))
#     'PCD' = Column(String(50))
#     'MIN BOLT (IF BLANK)' Column(SmallInteger)
#     'MAX BOLT (IF BLANK)' = Column(SmallInteger)
#     'MIN LUG (IF BLANK)' = Column(SmallInteger)
#     'MAX LUG (IF BLANK)' = Column(SmallInteger)
#     'ET' = Column(String(50))
#     'MIN ET' = Column(String(50))
#     'MAX ET' = Column(String(50))
#     'CB' = Column(Float)
#     'COLOUR' = Column(String(50))
#     'FINISH' = Column(String(50))
#     'WEIGHT LOAD (KG)' = Column(Float)
#     'WHEEL WEIGHT (KG)' = Column(Float)
#     'BOLT SEATING' = Column(SmallInteger)
#     'STAGGERED CODE' = Column(String(50))
#     'STAGGERED OPTION' = Column(String(50))
#     'STAGG UNIQUE SKU LOOKUP' = Column(String(50))
#     'STAGGERED POSITION' = Column(String(50))
#     'STAGGERED FRONT FILTER' = Column(String(50))
#     'QUANTITY (SETS AVAILABLE)' = Column(SmallInteger)
#     'SHIPPING WEIGHT' = Column(SmallInteger)
#     'SHIPPING (DOMESTIC)' = Column(Float)
#     'SHIPPING (INTERNATIONAL)' = Column(Float)
#     'MSRP' = Column(Float)
#     'PRICE MARK UP' = Column(Float)
#     'TOTAL UNIQUE PRICE (MSRP + MARGIN)' = Column(Float)
#     'B STOCK IDENTIFIER' = Column(String(50))
#     'DISCOUNTED PRICE' = Column(Float)
#     'SINGLE OR SET FILTER' = Column(String(50))
#     'IMPORT / DISPLAY FILTER' = Column(String(50))
#     'BRAND LOGO_[0]' = Column(String(500))
#     'BRAND BANNER' = Column(String(500))
#     'BRAND VIDEO 1' = Column(String(500))
#     'BRAND VIDEO 2' = Column(String(500))
#     'WHEEL DESCRIPTION' = Column(String(500))
#     'SEO KEYWORDS' = Column(String(500))
#     'GROUP IDENTIFIER' = Column(String(500))
#     __table_args__ = (
#         PrimaryKeyConstraint('SKU CODE (UNIQUE)', 'WHEEL OWNER'),
#         {},
#     )
#
#     def __repr__(self):
#         return f"User(id={self.'SKU CODE (UNIQUE)'!r}, name={self.'ITEM CODE'!r}, fullname={self.'IMAGE SKU 1'!r},...)"
