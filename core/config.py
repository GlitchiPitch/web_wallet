from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

class Database(BaseModel):
    url: PostgresDsn = f"postgresql+asyncpg://user:password@localhost:5432/wallet_db"

class WalletConfig(BaseModel):
    prefix: str = "/wallets"
    get_balance: str = "/{wallet_id}"
    deposit: str = get_balance + "/deposit"
    withdraw: str = get_balance + "/withdraw"

class ApiV1(BaseModel):
    prefix: str = "/v1"
    wallets: WalletConfig = WalletConfig()

class Api(BaseModel):
    prefix: str = "/api"
    v1: ApiV1 = ApiV1()

class Run(BaseModel):
    host: str = "localhost"
    port: int = 8000

class Settings(BaseSettings):
    db: Database = Database()
    api: Api = Api()
    run: Run = Run()

settings = Settings()