import sqlalchemy

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("login", sqlalchemy.String(100),nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String(100),nullable=False),
    sqlalchemy.Column("date", sqlalchemy.DateTime(),nullable=True),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean(), nullable=False),
)

messages_table = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.DateTime()),
    sqlalchemy.Column("SenderName", sqlalchemy.String(100)),
    sqlalchemy.Column("RecipientName", sqlalchemy.String(100)),
    sqlalchemy.Column("Messege", sqlalchemy.String(1024)),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
)