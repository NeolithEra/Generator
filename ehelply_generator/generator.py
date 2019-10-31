import json
from pathlib import Path
import re


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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

from typing import List, Union
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
    __tablename__ = \"{table}\"\n\n""".format(name=model['name'], table=model['table'])

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
                var_type: str = field['type'] + ", "

                if field['index']:
                    index: str = "primary_key=True, index=True, "
                else:
                    index: str = ""

                if field['nullable']:
                    nullable: str = "nullable=True, "
                else:
                    nullable: str = "nullable=False, "

                if field['unique']:
                    unique: str = "unique=True, "
                else:
                    unique: str = "unique=False, "

                if 'default' in field:
                    if type(field['default']) == str:
                        default: str = "default=\"" + field['default'] + "\", "
                    else:
                        default: str = "default=" + str(field['default']) + ", "
                else:
                    default: str = ""

                if 'foreign' in field:
                    cascade: str = ""
                    if 'cascade' in field['foreign'] and field['foreign']['cascade']:
                        cascade = ", ondelete='CASCADE'"
                    foreign: str = "ForeignKey('{name}'{cascade}), ".format(name=field['foreign']['name'], cascade=cascade)
                else:
                    foreign: str = ""

                self.model_content += """    {name} = Column({type}{foreign}{index}{unique}{nullable}{default})\n""".format(
                    name=name,
                    type=var_type,
                    foreign=foreign,
                    index=index,
                    unique=unique,
                    nullable=nullable,
                    default=default)
                if self.model_content.endswith(", )\n"):
                    self.model_content = self.model_content[:-4] + ")\n"

            for relation in model['relations']:
                self.model_content += """
    {name} = relationship(\"{model}\", back_populates=\"{populates}\", passive_deletes=True)\n""".format(name=relation['name'], populates=relation['populates'], model=relation['model'])

        self.model_content += "\n# END OF GENERATED CODE\n"

    def generate_schemas(self) -> None:
        for model in self.estructure['schemas']:
            for method in ["get", "create", "update", "db"]:
                self.schema_content += """

class {name}{method}(BaseModel):
    \"\"\"
    Used for {method}
    \"\"\"\n""".format(name=model['name'], method=method.capitalize())
                for field in model[method]:
                    default: str = ""
                    if not field['required']:
                        default = " = None"
                    self.schema_content += """    {name}: {type}{default}\n""".format(name=field['name'],
                                                                                      type=field['type'],
                                                                                      default=default)
                if method == "db":
                    self.schema_content += """
    class Config:
        orm_mode = True\n"""

        self.schema_content += "\n# END OF GENERATED CODE\n"

    def generate_crud(self) -> None:
        for model in self.estructure['cruds']:
            for method in ["get", "search", "create", "update", "delete"]:
                params: str = ""
                return_line: str = ""
                body: str = ""

                if method == "get":
                    key:str = "uuid"
                    if 'key' in model['get']:
                        key = model['get']['key']
                    params += ", {lil_name}_{key}: str".format(lil_name=convert(model['name']), key=key)
                    return_line += " -> models.{name}".format(name=model['name'])
                    body += """
    return db.query(models.{name}).filter(models.{name}.{key} == {lil_name}_{key}).first()""".format(name=model['name'], lil_name=convert(model['name']), key=key)

                if method == "search":
                    return_line += " -> List[models.{name}]".format(name=model['name'])
                    body += """
    return db.query(models.{name}).all()""".format(name=model['name'])

                if method == "delete":
                    key:str = "uuid"
                    if 'key' in model['delete']:
                        key = model['delete']['key']
                    params += ", {lil_name}_{key}: str".format(lil_name=convert(model['name']), key=key)
                    body += """
    db.query(models.{name}).filter(models.{name}.{key} == {lil_name}_{key}).delete()
    db.commit()""".format(name=model['name'], lil_name=convert(model['name']), key=key)

                if method == "create":
                    params += ", {lil_name}: schemas.{name}Db".format(lil_name=convert(model['name']), name=model['name'])
                    return_line += " -> models.{name}".format(name=model['name'])
                    body += """
    db_entry = models.{name}(**{lil_name}.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry""".format(name=model['name'], lil_name=convert(model['name']))

                if method == "update":
                    key:str = "uuid"
                    if 'key' in model['update']:
                        key = model['update']['key']
                    params += ", {lil_name}_{key}: str".format(lil_name=convert(model['name']), key=key)
                    params += ", {lil_name}: schemas.{name}Update".format(lil_name=convert(model['name']), name=model['name'])
                    return_line += " -> Union[models.{name}, None]".format(name=model['name'])
                    body += """
    if db.query(models.{name}).filter(models.{name}.{key} == {lil_name}_{key}).scalar() is not None:
        db_entry: models.{name} = db.query(models.{name}).filter(models.{name}.{key} == {lil_name}_{key}).first()\n""".format(name=model['name'], lil_name=convert(model['name']), key=key)
                    for field in model['fields']['update']:
                        if field['required']:
                            body += """
        db_entry.{field_name} = {lil_name}.{field_name}\n""".format(field_name = field['name'], lil_name=convert(model['name']))
                        else:
                            body += """
        if {lil_name}.{field_name} is not None:
            db_entry.{field_name} = {lil_name}.{field_name}\n""".format(field_name=field['name'], lil_name=convert(model['name']))
                    body += """ 
        db.commit()
        return db_entry
    else:
        return None"""

                self.crud_content += """
                
def {method}_{lil_name}(db: Session{params}){return_line}:
    \"\"\"
    Used to {method} {name}
    \"\"\"
    {body}\n""".format(method=method, lil_name=convert(model['name']), name=model['name'], params=params, return_line=return_line, body=body)

    def expand_structure(self) -> None:

        self.estructure = {
            "models": [],
            "schemas": [],
            "cruds": [],
        }

        for model in self.structure['models']:
            """
            Generic information per model
            """
            name: str = model['name']
            table: str = model['table']
            fields: list = model['fields']
            model_schema: dict = {
                "name": name,
                "table": table,
                "fields": [],
                "relations": [],
            }
            schema_schema: dict = {
                "name": name,
                "get": [],
                "create": [],
                "update": [],
                "db": [],
            }
            crud_schema: dict = {
                "name": name,
                "fields": {"update": []},
            }
            crud_schema.update(model['crud'])

            """
            MODEL FIELD INFORMATION SETUP
            """
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
                schema_field['name'] = field['name']

                """
                TYPE INFORMATION CHECKS BELOW
                """
                if field['type'] == 'uuid':
                    model_field['type'] = "String(64)"
                    model_field['unique'] = True
                    schema_field['type'] = "str"

                elif field['type'] == 'dict':
                    model_field['type'] = "JSON"
                    model_field['nullable'] = True
                    model_field['default'] = "{}"
                    schema_field['type'] = "dict"

                elif field['type'] == 'list':
                    model_field['type'] = "JSON"
                    model_field['nullable'] = True
                    model_field['default'] = "[]"
                    schema_field['type'] = "list"

                elif field['type'] == 'str':
                    length = "128"
                    if 'length' in field:
                        length = field['length']
                    model_field['type'] = "String({length})".format(length=length)
                    model_field['nullable'] = True
                    model_field['default'] = "{}"
                    schema_field['type'] = "str"

                elif field['type'] == 'id':
                    length = "64"
                    if 'length' in field:
                        length = field['length']
                    model_field['type'] = "String({length})".format(length=length)
                    model_field['nullable'] = True
                    schema_field['type'] = "str"

                elif field['type'] == 'text':
                    model_field['type'] = "Text"
                    model_field['nullable'] = True
                    schema_field['type'] = "str"

                elif field['type'] == 'int':
                    model_field['type'] = "Integer"
                    model_field['nullable'] = True
                    schema_field['type'] = "int"

                elif field['type'] == 'bool':
                    model_field['type'] = "Boolean"
                    model_field['default'] = "False"
                    schema_field['type'] = "bool"

                elif field['type'] == 'date':
                    model_field['type'] = "DateTime"
                    model_field['nullable'] = True
                    schema_field['type'] = "str"

                else:
                    print("Field has no valid type")
                    continue

                if 'default' in field:
                    model_field['default'] = field['default']
                    if model_field['default'] is None:
                        model_field['default'] = "None"

                if 'nullable' in field:
                    model_field['nullable'] = field['nullable']

                if 'index' in field:
                    model_field['index'] = field['index']

                if 'unique' in field:
                    model_field['unique'] = field['unique']

                if 'nullable' not in model_field:
                    model_field['nullable'] = False

                if 'index' not in model_field:
                    model_field['index'] = False

                if 'unique' not in model_field:
                    model_field['unique'] = False

                """
                RELATIONSHIPS
                """
                if 'relation' in field:
                    related_to: str = field['relation']['model']
                    related_key: str = field['relation']['key']
                    related_type: str = field['relation']['type']
                    related_cascade: bool = field['relation']['cascade']
                    for related_model in self.estructure['models']:
                        if related_model['name'] == related_to:
                            model_field['foreign'] = {
                                "name": related_model['table'] + "." + related_key,
                                "cascade": related_cascade
                            }
                            if related_type == "1:1":
                                model_schema['relations'].append({
                                    "name": convert(related_model['name']),
                                    "model": related_model['name'],
                                    "populates": convert(name)
                                })
                                related_model['relations'].append({
                                    "name": convert(name),
                                    "model": name,
                                    "populates": convert(related_model['name'])
                                })
                            else:
                                model_schema['relations'].append({
                                    "name": convert(related_model['name']),
                                    "model": related_model['name'],
                                    "populates": convert(name) + "s"
                                })
                                related_model['relations'].append({
                                    "name": convert(name) + "s",
                                    "model": name,
                                    "populates": convert(related_model['name'])
                                })
                            # TODO: Add a case n the IF statement above for auto generating pivot tables for n:n

                """
                FORMING SCHEMA FIELDS
                """

                if 'exclude_from_schema' not in field or not field['exclude_from_schema']:

                    # GET
                    for entry in model['schemas']['get']:
                        if type(entry) == str and entry == schema_field['name']:
                            schema_schema['get'].append({
                                'required': True,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })
                        elif type(entry) == dict and entry['field'] == schema_field['name']:
                            if 'required' in entry:
                                required = entry['required']
                            else:
                                required = True
                            schema_schema['get'].append({
                                'required': required,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })

                    # CREATE
                    for entry in model['schemas']['create']:
                        if type(entry) == str and entry == schema_field['name']:
                            schema_schema['create'].append({
                                'required': True,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })
                        elif type(entry) == dict and entry['field'] == schema_field['name']:
                            if 'required' in entry:
                                required = entry['required']
                            else:
                                required = True
                            schema_schema['create'].append({
                                'required': required,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })

                    # UPDATE
                    for entry in model['schemas']['update']:
                        if type(entry) == str and entry == schema_field['name']:
                            schema_schema['update'].append({
                                'required': False,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })
                            crud_schema['fields']['update'].append(
                                {
                                    'required': False,
                                    'name': schema_field['name']
                                }
                            )
                        elif type(entry) == dict and entry['field'] == schema_field['name']:
                            if 'required' in entry:
                                required = entry['required']
                            else:
                                required = False
                            schema_schema['update'].append({
                                'required': required,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })
                            crud_schema['fields']['update'].append(
                                {
                                    'required': False,
                                    'name': schema_field['name']
                                }
                            )

                    # DB
                    for entry in model['schemas']['db']:
                        if type(entry) == str and entry == schema_field['name']:
                            schema_schema['db'].append({
                                'required': True,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })
                        elif type(entry) == dict and entry['field'] == schema_field['name']:
                            if 'required' in entry:
                                required = entry['required']
                            else:
                                required = True
                            schema_schema['db'].append({
                                'required': required,
                                'name': schema_field['name'],
                                'type': schema_field['type']
                            })

                """
                WHITELISTING WHERE FIELDS BELONG
                """
                if 'exclude_from_model' not in field or not field['exclude_from_model']:
                    model_schema['fields'].append(model_field)

            self.estructure['models'].append(model_schema)
            self.estructure['schemas'].append(schema_schema)
            self.estructure['cruds'].append(crud_schema)

    def run(self) -> None:
        print("Input structure")
        print(json.dumps(self.structure, indent=2))
        self.expand_structure()
        print("\n\n\n\n\nExpanded structure")
        print(json.dumps(self.estructure, indent=2))

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
