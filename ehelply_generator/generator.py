import json
from pathlib import Path


class Generator:
    def __init__(self) -> None:
        self.structure_path: str = Path(Path(__file__).resolve().parents[1]).joinpath('structure.json')
        self.structure: dict = {}
        with open(self.structure_path, 'r') as file:
            self.structure = json.load(file)

        self.estructure: dict = {}

        self.model_base: str = """from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Text, DateTime 
from sqlalchemy.orm import relationship 
 
import uuid 
import datetime 
 
from ehelply_bootstrapper.utils.state import State
        """

        self.schema_base: str = """from typing import List, Dict, Tuple, Any 
 
from pydantic import BaseModel 
        """

        self.crud_base: str = """from sqlalchemy.orm import Session 
 
from . import models, schemas 
 
from ehelply_bootstrapper.utils.state import State 
        """

        self.model_content: str = self.model_base
        self.schema_content: str = self.schema_base
        self.crud_content: str = self.crud_base

    def generate_models(self) -> None:
        for model in self.estructure['models']:
            self.model_content += """

class {name}(State.mysql.Base):
    \"\"\"
    Represents a {name}
    \"\"\"
    __tablename__ = \"{table}\"\n""".format(name=model['name'], table=model['table'])

        for field in model['fields']:
            """
            name
            type.
            index
            nullable
            default
            unique
            """

            name: str = field['name']
            type: str = field['type'] + ","

            if field['index']:
                index: str = "primary_key=True,index=True,"
            else:
                index: str = ""

            if field['nullable']:
                nullable: str = "nullable=True,"
            else:
                nullable: str = "nullable=False,"

            if field['unique']:
                unique: str = "unique=True,"
            else:
                unique: str = "unique=False,"

            if 'default' in field:
                default: str = "default=\"" + field['default'] + "\","
            else:
                default: str = ""

            self.model_content += """    {name} = Column({type}{index}{unique}{nullable}{default})\n""".format(
                name=name,
                type=type,
                index=index,
                unique=unique,
                nullable=nullable,
                default=default)

        self.model_content += "\n# END OF GENERATED CODE\n"

    def generate_schemas(self) -> None:
        self.schema_content += "\n# END OF GENERATED CODE\n"

    def generate_crud(self) -> None:
        self.crud_content += "\n# END OF GENERATED CODE\n"

    def expand_structure(self) -> None:

        self.estructure = {
            "models": [],
            "schemas": [],
            "cruds": [],
        }

        for model in self.structure['models']:
            name: str = model['name']
            table: str = model['table']
            fields: list = model['fields']
            model_schema: dict = {
                "name": name,
                "table": table,
                "fields": [],
            }
            schema_schema: dict = {
                "name": name,
                "fields": [],
            }
            crud_schema: dict = {
                "name": name,
                "fields": [],
            }
            for field in fields:
                """
                Types:
                uuid   -> String, str     -> index(True)
                dict   -> JSON, dict      -> nullable(True), default({})
                list   -> JSON, dict      -> nullable(True), default([])
                str    -> String, str     -> length(128), nullable(False), default()
                id     -> String, str     -> length(64), nullable(False), default()
                text   -> Text, str       -> nullable(True), default()
                int    -> Integer, int    -> nullable(True)
                bool   -> Boolean, bool   -> default(False)
                date   -> DateTime, str   -> nullable(True)
                """
                model_field: dict = {}
                schema_field: dict = {}
                crud_field: dict = {}

                model_field['name'] = field['name']

                if field['type'] == 'uuid':
                    model_field['type'] = "String(64)"

                elif field['type'] == 'dict':
                    model_field['type'] = "JSON"
                    model_field['nullable'] = True
                    model_field['default'] = "{}"

                elif field['type'] == 'list':
                    model_field['type'] = "JSON"
                    model_field['nullable'] = True
                    model_field['default'] = "[]"

                elif field['type'] == 'str':
                    length = "128"
                    if 'length' in field:
                        length = field['length']
                    model_field['type'] = "String({length})".format(length=length)
                    model_field['nullable'] = True
                    model_field['default'] = "{}"

                elif field['type'] == 'id':
                    length = "64"
                    if 'length' in field:
                        length = field['length']
                    model_field['type'] = "String({length})".format(length=length)
                    model_field['nullable'] = True
                    model_field['default'] = "{}"

                elif field['type'] == 'text':
                    model_field['type'] = "Text"
                    model_field['nullable'] = True

                elif field['type'] == 'int':
                    model_field['type'] = "Integer"
                    model_field['nullable'] = True

                elif field['type'] == 'bool':
                    model_field['type'] = "Boolean"
                    model_field['default'] = "False"

                elif field['type'] == 'date':
                    model_field['type'] = "DateTime"
                    model_field['nullable'] = True
                else:
                    print("Field has no valid type")
                    continue

                if 'default' in field:
                    model_field['default'] = field['default']
                    if model_field['default'] is None:
                        model_field['default'] = "None"

                if 'nullable' in field and field['nullable']:
                    model_field['nullable'] = True
                else:
                    model_field['nullable'] = False

                if 'index' in field and field['index']:
                    model_field['index'] = True
                else:
                    model_field['index'] = False

                if 'unique' in field and field['unique']:
                    model_field['unique'] = True
                else:
                    model_field['unique'] = False

                model_schema['fields'].append(model_field)
                schema_schema['fields'].append(schema_field)
                crud_schema['fields'].append(crud_field)

            self.estructure['models'].append(model_schema)
            self.estructure['schemas'].append(schema_schema)
            self.estructure['cruds'].append(crud_schema)

    def run(self) -> None:
        print(self.structure)
        self.expand_structure()

        self.generate_models()
        self.generate_schemas()
        self.generate_crud()

        self.write_file("crud.py", self.crud_content)
        self.write_file("models.py", self.model_content)
        self.write_file("schemas.py", self.schema_content)

    def write_file(self, name: str, content: str) -> None:
        path: str = Path(Path(__file__).resolve().parents[1]).joinpath('output').joinpath(name)
        with open(path, 'w') as file:
            file.write(content)


if __name__ == "__main__":
    generator = Generator()
    generator.run()
