Reflect DB Schema
=================

::

  import streamlit as st
  from sqlalchemy import create_engine, MetaData
  from pathlib import Path
  import yaml

Read DB configuration

::

  db_config_file = Path("alchem.yml")
  if db_config_file.exists():
      with open(db_config_file, 'r') as file:
          db_config = yaml.safe_load(file)
      db_name = db_config["db_name"]
      db_user = db_config["db_user"]
      db_pass = db_config["db_pass"]
      db_schema = db_config["db_schema"]
    
  db_name = st.text_input("db name", db_name)    
  db_user = st.text_input("db user", db_user)
  db_pass = st.text_input("db pass", db_pass)
  db_schema = st.text_input("db schema", db_schema)

  metadata = MetaData(schema=db_schema)

Reflect DB Schema

::

  if st.button("Reflect schema", type="primary", width="stretch"): 

      DATABASE_URL = f"postgresql+psycopg://{db_user}:{db_pass}@localhost:5432/{db_name}"
    
      engine = create_engine(
          DATABASE_URL,
          echo=False,
          pool_pre_ping=True,
      )
    
      metadata.reflect(bind=engine)
      st.write(metadata.tables.keys())    