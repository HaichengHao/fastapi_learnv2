# @Time    : 2026/1/28 09:45
# @Author  : hero
# @File    : settings.py
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    model_config=SettingsConfigDict(  #指定模型的配置字典
        env_file='.env', #tips:读取env文件作为配置源
        extra="ignore" #tips:忽略其它来源的配置
    )


#实例化类对象
project_configs=Settings()
print(project_configs.DATABASE_URL)

