# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Text, DateTime

# from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class WhatismybrowserUseragentModel(Base):
    """Created automatically via `sqlacodegen`"""

    __tablename__ = "whatismybrowser_useragent"

    id = Column(Integer, primary_key=True)
    user_agent = Column(Text())
    times_seen = Column(Integer, nullable=False)
    simple_software_string = Column(String(255))
    simple_sub_description_string = Column(String(255))
    simple_operating_platform_string = Column(String(255))
    software = Column(String(255))
    software_name = Column(String(255))
    software_name_code = Column(String(255))
    software_version = Column(String(255))
    software_version_full = Column(String(255))
    operating_system = Column(String(255))
    operating_system_name = Column(String(255))
    operating_system_name_code = Column(String(255))
    operating_system_version = Column(String(255))
    operating_system_version_full = Column(String(255))
    operating_system_flavour = Column(String(255))
    operating_system_flavour_code = Column(String(255))
    operating_system_frameworks = Column(Text())
    operating_platform = Column(String(255))
    operating_platform_code = Column(String(255))
    operating_platform_code_name = Column(String(255))
    operating_platform_vendor_name = Column(String(255))
    software_type = Column(String(255))
    software_sub_type = Column(String(255))
    software_type_specific = Column(String(255))
    hardware_type = Column(String(255))
    hardware_sub_type = Column(String(255))
    hardware_sub_sub_type = Column(String(255))
    hardware_type_specific = Column(String(255))
    layout_engine_name = Column(String(255))
    layout_engine_version = Column(String(255))
    extra_info = Column(Text())
    extra_info_dict = Column(Text())
    capabilities = Column(Text())
    detected_addons = Column(Text())
    first_seen_at = Column(DateTime, nullable=False)
    last_seen_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    def __repr__(self):
        return "<UserAgent(ua='{}', times_seen='{}')>".format(
            self.user_agent, self.times_seen
        )


'''
class MYSQLWhatismybrowserUseragentModel(Base):
    """Created automatically via `sqlacodegen`"""

    __tablename__ = "whatismybrowser_useragent"

    id = Column(Integer, primary_key=True)
    user_agent = Column(LONGTEXT)
    times_seen = Column(Integer, nullable=False)
    simple_software_string = Column(String(255))
    simple_sub_description_string = Column(String(255))
    simple_operating_platform_string = Column(String(255))
    software = Column(String(255))
    software_name = Column(String(255))
    software_name_code = Column(String(255))
    software_version = Column(String(255))
    software_version_full = Column(String(255))
    operating_system = Column(String(255))
    operating_system_name = Column(String(255))
    operating_system_name_code = Column(String(255))
    operating_system_version = Column(String(255))
    operating_system_version_full = Column(String(255))
    operating_system_flavour = Column(String(255))
    operating_system_flavour_code = Column(String(255))
    operating_system_frameworks = Column(LONGTEXT)
    operating_platform = Column(String(255))
    operating_platform_code = Column(String(255))
    operating_platform_code_name = Column(String(255))
    operating_platform_vendor_name = Column(String(255))
    software_type = Column(String(255))
    software_sub_type = Column(String(255))
    software_type_specific = Column(String(255))
    hardware_type = Column(String(255))
    hardware_sub_type = Column(String(255))
    hardware_sub_sub_type = Column(String(255))
    hardware_type_specific = Column(String(255))
    layout_engine_name = Column(String(255))
    layout_engine_version = Column(String(255))
    extra_info = Column(LONGTEXT)
    extra_info_dict = Column(LONGTEXT)
    capabilities = Column(LONGTEXT)
    detected_addons = Column(LONGTEXT)
    first_seen_at = Column(DATETIME(fsp=6), nullable=False)
    last_seen_at = Column(DATETIME(fsp=6), nullable=False)
    updated_at = Column(DATETIME(fsp=6))

    def __repr__(self):
        return "<UserAgent(ua='{}', times_seen='{}')>".format(
            self.user_agent, self.times_seen
        )
'''
