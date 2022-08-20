from openapi_schema_pydantic.util import PydanticSchema


class SomeSchema:
    pass


HANDWRITTEN_METHODS_MAP = {'api_name': {    # указать имя описываемого апи метода
                                    "/api/{api_group_name}/{api_name}": {  # ссылка на описываемый апи метод
                                        "post": {
                                            "description": 'API_MAP_V1["api_group_name"]["api_name"]["description"]', # Пояснение к описываемому апи методу
                                            "requestBody": {"content": {"application/json": {
                                                "schema": PydanticSchema(schema_class=SomeSchema)   # Pydantic схема запроса
                                            }}},
                                            "responses": {"200": {  # код ответа
                                                "description": 'API_MAP_V1["api_group_name"]["api_name"]["description"]', # Пояснение к ответу описываемого апи метода
                                                "content": {
                                                    "application/json": {
                                                        "schema": {     # Схема возвращаемого объекта, описанная вручную
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "type": "integer",
                                                                    "description": "The user ID."
                                                                },
                                                                "username": {
                                                                    "type": "string",
                                                                    "description": "The user name."
                                                                }
                                                            }
                                                        }
                                                    }
                                                }},
                                            }},
                                        }
                                    },
                                    'add_customer': {    # указать имя описываемого апи метода
                                        "/api/save_customer": {  # ссылка на описываемый апи метод
                                            "post": {
                                                "description": 'Добавление заказчика', # Пояснение к описываемому апи методу
                                                "requestBody": {"content": {"application/json": {
                                                    "schema": {     # Схема возвращаемого объекта, описанная вручную email, phone, name, bid_type
                                                            "type": "object",
                                                            "properties": {
                                                                "email": {
                                                                    "type": "string"
                                                                },
                                                                "phone": {
                                                                    "type": "string"
                                                                },
                                                                "name": {
                                                                    "type": "string"
                                                                },
                                                                "bid_type": {
                                                                    "type": "string",
                                                                    "description": "Тип заказа "
                                                                                   "\n 1 - разработка сайта"
                                                                                   "\n 2 - разработка телеграм бота"
                                                                                   "\n 3 - дизайн"
                                                                                   "\n 3 - постпродакшн"
                                                                },
                                                            }
                                                        }
                                                }}},
                                                "responses": {"200": {  # код ответа
                                                    "description": 'заказчик добавлен', # Пояснение к ответу описываемого апи метода

                                                },
                                                }},
                                            }
                                        },
                                    'get_customers': {    # указать имя описываемого апи метода
                                        "/api/get_customers": {  # ссылка на описываемый апи метод
                                            "get": {
                                                "description": 'Получение всех заказчиков', # Пояснение к описываемому апи методу
                                                "responses": {"200": {  # код ответа
                                                    "description": 'список заказчиков', # Пояснение к ответу описываемого апи метода

                                                },
                                                }},
                                            }
                                        },
                                    'get_customer_by_id': {    # указать имя описываемого апи метода
                                        "/api/get_customer/<id>": {  # ссылка на описываемый апи метод
                                            "get": {
                                                "description": 'Получение заказчика по id', # Пояснение к описываемому апи методу
                                                "requestBody": {"content": {"application/json": {
                                                    "schema": {     # Схема возвращаемого объекта, описанная вручную email, phone, name, bid_type
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "type": "integer"
                                                                }
                                                            }
                                                        }
                                                }}},
                                                "responses": {"200": {  # код ответа
                                                    "description": 'список заказчиков', # Пояснение к ответу описываемого апи метода

                                                },
                                                }},
                                            }
                                        },
                                    'get_customer_by_phone': {    # указать имя описываемого апи метода
                                        "/api/get_customer/<phone>": {  # ссылка на описываемый апи метод
                                            "get": {
                                                "description": 'Получение заказчика по номеру телефона', # Пояснение к описываемому апи методу
                                                "requestBody": {"content": {"application/json": {
                                                    "schema": {     # Схема возвращаемого объекта, описанная вручную email, phone, name, bid_type
                                                            "type": "object",
                                                            "properties": {
                                                                "phone": {
                                                                    "type": "integer"
                                                                }
                                                            }
                                                        }
                                                }}},
                                                "responses": {"200": {  # код ответа
                                                    "description": 'список заказчиков', # Пояснение к ответу описываемого апи метода

                                                },
                                                }},
                                            }
                                        },
                                    'delete_customer': {    # указать имя описываемого апи метода
                                        "/api/delete_customer": {  # ссылка на описываемый апи метод
                                            "delete": {
                                                "description": 'Получение заказчика по номеру телефона', # Пояснение к описываемому апи методу
                                                "requestBody": {"content": {"application/json": {
                                                    "schema": {     # Схема возвращаемого объекта, описанная вручную email, phone, name, bid_type
                                                            "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer"
                                                            }
                                                        }
                                                        }
                                                }}},
                                                "responses": {"200": {  # код ответа
                                                    "description": 'список заказчиков', # Пояснение к ответу описываемого апи метода

                                                },
                                                }},
                                            }
                                        }
                                    }