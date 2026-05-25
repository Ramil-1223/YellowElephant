from pydantic import BaseModel, Field


class CreateDB(BaseModel):
    description: str = Field(min_length=1, max_length=30)
    port: str
    cluster_id: str
    dbname: str = Field(
        min_length=1, max_length=20, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    )


class BackupDB(BaseModel):
    backup_format: str
    backup_dir: str
    dbname: str = Field(
        min_length=1, max_length=20, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    )


class DropDB1C(BaseModel):
    cluster: str
    dbname: str = Field(
        min_length=1, max_length=20, pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    )
