# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RbacInterface(Base):
    __tablename__ = 'rbac_interface'

    id = Column(String(40), primary_key=True)
    name = Column(String(64), nullable=False)
    path = Column(String(64), nullable=False)
    method = Column(String(16), nullable=False)
    desc = Column(String(64), nullable=False)


class RbacMenu(Base):
    __tablename__ = 'rbac_menu'

    id = Column(String(40), primary_key=True)
    parentId = Column(String(40), nullable=False)
    path = Column(String(36), nullable=False)
    title = Column(String(36), nullable=False)
    icon = Column(String(36), nullable=False)
    permission = Column(String(64), nullable=False)
    type = Column(INTEGER(1), nullable=False)
    sort = Column(INTEGER(3), nullable=False)
    isLock = Column(TINYINT(1), nullable=False)
    desc = Column(String(128), nullable=False)


class RbacRole(Base):
    __tablename__ = 'rbac_role'

    id = Column(String(40), primary_key=True)
    name = Column(String(16), nullable=False)
    code = Column(String(64), nullable=False)
    isLock = Column(TINYINT(1), nullable=False)
    desc = Column(String(64), nullable=False)


class RbacRoute(Base):
    __tablename__ = 'rbac_route'

    id = Column(String(40), primary_key=True)
    parentId = Column(String(40), nullable=False)
    path = Column(String(36), nullable=False)
    name = Column(String(36), nullable=False)
    title = Column(String(36), nullable=False)
    permission = Column(String(64), nullable=False)
    component = Column(String(36), nullable=False)
    componentPath = Column(String(36), nullable=False)
    sort = Column(INTEGER(11), nullable=False)
    isLock = Column(TINYINT(1), nullable=False)
    cache = Column(TINYINT(1), nullable=False)


class RbacUser(Base):
    __tablename__ = 'rbac_user'

    id = Column(String(40), primary_key=True)
    name = Column(String(64), nullable=False)
    realName = Column(String(16), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(64))
    phone = Column(String(32))
    isLock = Column(TINYINT(1))
    create_at = Column(DateTime, nullable=False)


class RbacFunctioninterface(Base):
    __tablename__ = 'rbac_functioninterface'

    id = Column(String(40), primary_key=True)
    interfaceId = Column(ForeignKey('rbac_interface.id'), nullable=False, index=True)
    menuId = Column(ForeignKey('rbac_menu.id'), nullable=False, index=True)

    rbac_interface = relationship('RbacInterface')
    rbac_menu = relationship('RbacMenu')


class RbacRolefunction(Base):
    __tablename__ = 'rbac_rolefunction'

    id = Column(String(40), primary_key=True)
    roleId = Column(ForeignKey('rbac_role.id'), nullable=False, index=True)
    menuId = Column(ForeignKey('rbac_menu.id'), nullable=False, index=True)

    rbac_menu = relationship('RbacMenu')
    rbac_role = relationship('RbacRole')


class RbacRoleuser(Base):
    __tablename__ = 'rbac_roleuser'

    id = Column(String(64), primary_key=True)
    userId = Column(ForeignKey('rbac_user.id'), nullable=False, index=True)
    roleId = Column(ForeignKey('rbac_role.id'), nullable=False, index=True)

    rbac_role = relationship('RbacRole')
    rbac_user = relationship('RbacUser')
