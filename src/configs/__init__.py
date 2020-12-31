from typing import Optional

from pydantic import BaseSettings

INDEX_RESPONSE = """
                              ▄▄▄▄▄                  _________________
                              ▀▀▀██████▄▄▄          /  Bigpearl       \\
                            ▄▄▄▄▄  █████████▄       |  Gotta go fast! |
                            ▀▀▀▀█████▌ ▀▐▄ ▀▐█      | ________________/
                          ▀▀█████▄▄ ▀██████▄██      |/ 
                          ▀▄▄▄▄▄  ▀▀█▄▀█════█▀         
                              ▀▀▀▄  ▀▀███ ▀      ▄▄   
                            ▄███▀▀██▄████████▄ ▄▀▀▀██▌ 
                          ██▀▄▄▄██▀▄███▀ ▀▀████     ▀█▄
                      ▄▀▀▀▄██▄▀▀▌████▒▒▒▒▒▒███    ▌▄▄▀
                      ▌    ▐▀████▐███▒▒▒▒▒▐██▌        
                      ▀▄  ▄▀   ▀▀████▒▒▒▒▄██▀         
                        ▀▀      ▀▀█████████▀          
                              ▄▄██▀██████▀█           
                            ▄██▀     ▀▀▀  █           
                            ▄█             ▐▌          
                        ▄▄▄▄█▌              ▀█▄▄▄▄▀▀▄  
                       ▌     ▐                ▀▀▄▄▄▀   
                        ▀▀▄▄▀                          
        """


class Settings(BaseSettings):
    env: str = "local"
    dynamodb_add_table_name: str = "add_table"
    redis_url: str = "redis://localhost:6379/0?encoding=utf-8"
    kafka_endpoint: str = "localhost:9092"
    kafka_topic: str = ""
    redoc_path: Optional[str] = "/redoc"
    docs_path: Optional[str] = "/docs"

    def __init__(self, **values):
        super().__init__(**values)
        self.kafka_topic = f"kafka-topic-{self.env}"
        if self.env == "prod":
            self.redoc_path = None
            self.docs_path = None


settings = Settings()
