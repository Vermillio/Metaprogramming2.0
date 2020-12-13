import os
import sqlite3
import class_structure_example

python_to_sql_types = {
    type(11): "INTEGER",
    type("ta"): "TEXT",
    type(1.1): "REAL",
    type(True): "INTEGER",  # SQLite stores bool values as integers
    type(None): "NULL"
}


def get_sql_type(python_type: type) -> str:
    return python_to_sql_types[python_type]


def is_list(python_type: type) -> bool:
    list_obj = []
    return isinstance(python_type(), type(list_obj))

class Py2SQL:

    tables_dict = {}
    table_counts = {}
    logging = True

    def __init__(self):
        self.connection = None

    def db_connect(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.db_path = db_path
        self.db_update()

    def db_update(self):
        tables = self.db_tables()
        for t in tables:
            self.tables_dict[t] = []
            self.table_counts[t] = self.db_table_count(t)

    def db_disconnect(self):
        if self.connection:
            self.connection.close()
        self.db_path = None
        self.tables_dict = {}
        self.table_counts = {}

    def db_name(self):
        return self.db_path

    def db_size_Mb(self):
        if self.db_path:
            return os.path.getsize(self.db_path) / (1024.0 * 1024.0)

    def db_tables(self):
        if self.connection:
            c = self.connection.cursor()
            tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            return [t[0] for t in tables]
        return None

    def db_table_structure(self, table):
        return NotImplemented

    def db_table_count(self, table):
        if self.connection:
            c = self.connection.cursor()
            return len(c.execute(f'select * from {table};').fetchall())
        return None

    def db_table_counts(self):
        return self.table_counts

    def save_object(self, object):
        if self.connection:
            c = self.connection.cursor()
            query = self._map_object(object)
            if self.logging:
                print(query)
            c.executescript(query)
            return True
        return False

    def save_class(self, cls):
        if self.connection:
            c = self.connection.cursor()
            query = self._map_class(cls)
            if self.logging:
                print(query)
            c.executescript(query)
            return True
        return False

    def save_hierarchy(self, root_cls):
        if self.connection:
            c = self.connection.cursor()
            query = self._map_class(cls)
            c.executescript(query)
            get_all_subclasses = lambda cls: set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in get_all_subclasses(c)])
            subclasses = get_all_subclasses(root_cls)
            for s in subclasses:
                query = self._map_class(s)
                c.executescript(query)
            return True
        return False

    def delete_object(self, object):
        if self.connection:
            c = self.connection.cursor()
            c.execute(f'DELETE FROM {type(object).__name__} WHERE ObjectId={id(object)}' )
            return True
        return False

    def delete_class(self, cls):
        if self.connection:
            c = self.connection.cursor()
            cls_name=cls.__name__
            query=f'DROP TABLE IF EXISTS {cls_name};'
            for other_table in self.tables_dict[cls_name]:
                query+=f'DROP TABLE IF EXISTS {cls_name}_{other_table};'
                query+=f'DROP TABLE IF EXISTS {other_table}_{cls_name};'
                self.tables_dict[other_table].remove(cls_name)
            self.tables_dict.pop(cls_name)
            c.execute(query)
            return True
        return False

    def delete_hierarchy(self, root_class):
        if self.connection:
            c = self.connection.cursor()
            get_all_subclasses = lambda cls: set(cls.__subclasses__()).union(
                [s for c in cls.__subclasses__() for s in get_all_subclasses(c)])
            subclasses = get_all_subclasses(root_cls)
            for s in subclasses:
                self.delete_class(s)
            return True
        return False

    def _map_object(self, o : object):
        queries = []
        if is_list(type(o)):
            return self._map_list(o)
        else:
            return self._map_list([o])

    def _map_list(self, objects: list) -> str:
        if len(objects) == 0:
            return ""
        o = objects[0]

        table_name = type(o).__name__
        attributes = o.__dict__
        attribute_names = "ObjectId"
        attributes = [att for att in attributes if not att.startswith('__')]
        for i in range(len(attributes)):
            attr = attributes[i]
            var = o.__dict__[attr]
            if not is_list(type(var)):
                if type(var) == str:
                    attribute_names += f", {attr}"
                else:
                    try:
                        python_to_sql_types[type(var)]
                        attribute_names += f", {attr}"
                    except KeyError:
                        attribute_names += f", {type(var).__name__}Id"

        queries = []
        objects_strings = []
        obj_id = self.table_counts[type(o).__name__]
        for obj in objects:
            self.table_counts[type(o).__name__]+=1;
            s = f"({self._get_sqlite_type_repr(id(obj), queries, table_name, obj_id)}"
            for i in range(len(attributes)):
                a = attributes[i]
                repr = self._get_sqlite_type_repr(o.__dict__[a], queries, table_name, obj_id)
                if repr != "":
                    s += f", {repr}"
            obj_id+=1
            s += ")"
            objects_strings.append(s)

        for obj_str in objects_strings:
            obj_str = "\n\t\t" + obj_str
        values = ','.join(objects_strings)

        res = "".join(queries)
        res += f"""\nINSERT INTO {table_name}({attribute_names})\n\tVALUES {values};"""

        return res


    def _get_sqlite_type_repr(self, var, queries=[], parent="", parent_id=1) -> str:
        if type(var) == str:
            return f"\"{var}\""
        try:
            python_to_sql_types[type(var)]
            return var
        except KeyError:
            var_name = type(var[0]).__name__ if is_list(type(var)) else type(var).__name__
            id = self.table_counts[var_name]
            queries.append(self._map_object(var))
            if is_list(type(var)):
                # creating record in connection table
                values = []
                for item in var:
                    values.append(f"\n\t\t({parent_id}, {id})")
                    id += 1
                values_str = ','.join(values)
                connection = f"""\nINSERT INTO {parent}_{var_name} ({parent}Id, {var_name}Id) VALUES {values_str};"""
                self.table_counts[f'{parent}_{var_name}'] += len(values)
                queries.append(connection)
                return ""
            max_q = f"""(SELECT MAX({var_name}Id) FROM {var_name})"""
            return max_q

    def _get_inner_relation(self, inner_name):
        table_relation_to_inner_table = f",\n\t\t[{inner_name}Id] INTEGER NOT NULL"
        table_relation_to_inner_table += f",\n\t\tFOREIGN KEY ([{inner_name}Id]) REFERENCES \"{inner_name}\"([{inner_name}Id])"
        table_relation_to_inner_table += f"\n\t\t\t\tON DELETE NO ACTION ON UPDATE NO ACTION"
        return table_relation_to_inner_table


    def _get_outer_relation(self, table_name):
        remote_relation = f",\n\t\t[{table_name}] INTEGER NOT NULL"
        remote_relation += f",\n\t\tFOREIGN KEY ([{table_name}Id]) REFERENCES \"{table_name}\"([{table_name}Id])"
        remote_relation += f"\n\t\t\t\tON DELETE NO ACTION ON UPDATE NO ACTION"
        return remote_relation


    # Adds queries for inner object class and for connection table to @inner_table_queries
    def build_many_to_many_relation(self, inner_table_queries, inner_type, table_name):
        inner_name = inner_type.__name__
        inner_query = self._map_class(inner_type)
        self.tables_dict[inner_name].append(table_name)
        self.tables_dict[table_name].append(inner_name)
        self.table_counts[f'{table_name}_{inner_name}'] = 0
        # Creating table for inner object class if needed
        inner_table_queries.append(inner_query)
        # Creating connection table
        connection_table_query = self.get_connection_table(inner_name, table_name)
        inner_table_queries.append(connection_table_query)


    def get_connection_table(self, inner_name, table_name):
        connection_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name}_{inner_name}
        (
            {table_name}Id INTEGER,
            {inner_name}Id INTEGER,
            FOREIGN KEY({table_name}Id) REFERENCES \"{table_name}\"({table_name}Id),
            FOREIGN KEY({inner_name}Id) REFERENCES \"{inner_name}\"({inner_name}Id)
        );
                            """
        return connection_table_query

    def _map_class(self, class_type: type, parent_relation="") -> str:
        class_object = class_type()
        attributes = class_object.__dict__
        table_name = class_type.__name__

        self.tables_dict[table_name] = []
        self.table_counts[table_name] = 0
        inner_table_queries = []

        # Every table gets new id by default even if it class had field like Id, ClassId etc.
        table_fields = f"\t[{table_name}Id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"
        table_fields+=",\n\t\t[ObjectId] INTEGER"
        for attr in attributes:
            if not attr.startswith('__'):
                try:
                    table_fields += f",\n\t\t[{attr}] {get_sql_type(type(attributes[attr]))}"
                # We did not find SQLite translatable type so it must be object of other type call it @inner_class
                except KeyError:
                    # Actions if we saw inner class list - many to many relation or one to many (we take it as same)
                    if is_list(type(attributes[attr])):
                        if len(attributes[attr]) == 0:
                            continue
                        else:
                            inner_type = type(attributes[attr][0])
                            self.build_many_to_many_relation(inner_table_queries, inner_type, table_name)

                    # Actions if we saw inner class object - one to one relation
                    else:
                        inner_name = type(attributes[attr]).__name__
                        relation_to_inner_table = self._get_inner_relation(inner_name)
                        table_fields += relation_to_inner_table
                        # Relation passed to inner class table as foreign key to connect with parent on one to one basis
                        #remote_relation = self._get_outer_relation(table_name)

                        inner_query = self._map_class(type(attributes[attr]))#, parent_relation=remote_relation)
                        inner_table_queries.append(inner_query)

        query_string = ""
        class_query = f"""CREATE TABLE IF NOT EXISTS {table_name}
        (
        {table_fields}{parent_relation}
        );"""
        inner_table_queries.reverse()
        for inner_query in inner_table_queries:
            query_string += f"\n\n{inner_query}"
        query_string += f"\n\n{class_query}"
        return query_string


print(py2sql._map_object(class_structure_example.User()))
print(py2sql._map_object(class_structure_example.User()))

print(class_structure_example.User.__dict__)

py2sql = Py2SQL()
py2sql.db_connect('my.db')
py2sql.db_name()
py2sql.save_class(class_structure_example.User)
py2sql.db_size_Mb()
py2sql.db_tables()
py2sql.db_table_counts()
py2sql.db_update()
py2sql.save_object(class_structure_example.User())
