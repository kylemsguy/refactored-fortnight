from sqlalchemy import create_engine, event as saevent
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy import ForeignKey, Column, Index, Table
from sqlalchemy import Integer, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, BIT, ENUM, JSON
from sqlalchemy.types import CHAR, FLOAT, TIMESTAMP, VARCHAR
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import os

engine_uri = 'postgres://appuser:dHknxPX7vp+QksWSMgy0PQp82CnHbHxNAQrZbtJH4eo=@refactored-fortnight-1.cieg7bqkdceo.us-east-1.rds.amazonaws.com/hackathonsim'
engine = create_engine(engine_uri,
                       echo=False,
                       pool_size=100,  # unlimited
                       pool_recycle=-1,  # recycle with no timeout
                       pool_timeout=10)  # 10 seconds





# The session factory is private, and not to be accessed directly
_sessionFactory = sessionmaker()
_sessionFactory.configure(bind=engine)

# This `session` is a proxy that can be accessed and used anywhere
# All sessions made from this are in actuality, the same session.
# Scoped sessions are also thread-safe, actual sessions are not.
Session = scoped_session(_sessionFactory)
Base = declarative_base()
