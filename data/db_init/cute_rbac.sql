-- Adminer 4.6.3 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `rbac_functioninterface`;
CREATE TABLE `rbac_functioninterface` (
  `id` varchar(40) NOT NULL,
  `interfaceId` varchar(40) NOT NULL,
  `menuId` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_rbac_functioninterface_interfaceId` (`interfaceId`),
  KEY `ix_rbac_functioninterface_menuId` (`menuId`),
  CONSTRAINT `rbac_functioninterface_ibfk_1` FOREIGN KEY (`interfaceId`) REFERENCES `rbac_interface` (`id`),
  CONSTRAINT `rbac_functioninterface_ibfk_2` FOREIGN KEY (`menuId`) REFERENCES `rbac_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `rbac_interface`;
CREATE TABLE `rbac_interface` (
  `id` varchar(40) NOT NULL,
  `name` varchar(64) NOT NULL,
  `path` varchar(64) NOT NULL,
  `method` varchar(16) NOT NULL,
  `desc` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `rbac_interface` (`id`, `name`, `path`, `method`, `desc`) VALUES
('0317ee55-c941-4cde-950b-3943e3941bb6',	'保存接口',	'/rbac/interface/',	'post',	'保存接口信息'),
('061360da-42ea-4ced-a389-d1d84d5be561',	'用户密码修改[管理]',	'/rbac/user/adminchangepassword',	'post',	'管理员直接修改用户密码'),
('06e60a5a-6e8b-46ef-8bbb-b9c8505eac93',	'用户批量删除',	'/rbac/user/batchdel',	'delete',	'用户批量删除'),
('07e63371-4d47-4f0b-a389-0e873d7f8cd7',	'用户删除',	'/rbac/user/del',	'delete',	'根据ID删除用户'),
('08437312-0c3a-4d76-84da-72b4d0902ee4',	'菜单列表获取',	'/rbac/menu',	'get',	'查看菜单信息'),
('1a7fb5df-9392-4a59-b654-5d1c301e2316',	'用户添加',	'/rbac/user/save',	'post',	'添加用户'),
('1dc000a8-89af-49b6-a930-9ee81a8066d9',	'路由信息',	'/rabc/route/:id',	'get',	'根据ID获取路由信息'),
('22e5b39c-1e89-4881-9b1d-3deae5496298',	'角色列表',	'/rbac/role/',	'get',	'获取角色列表'),
('3e9697ec-ffcb-4f92-9deb-c10d7cd7c91c',	'接口ID信息',	'/rbac/interface/:id',	'get',	'根据ID查看菜单信息'),
('428c359b-aa1a-4987-9087-67b58faed3c9',	'角色权限保存',	'/rbac/role/savepermission/',	'post',	'保存角色权限'),
('5378c831-6e86-4f96-9ac7-2fec85d7ff05',	'用户修改密码',	'/rbac/user/changepassword',	'post',	'修改自己的密码'),
('5b2f1df5-db0b-47b4-b2d7-e3ad063a8866',	'角色权限获取',	'/rbac/role/permissions/:id',	'get',	'根据ID获取角色已经有的权限'),
('668a3300-7706-4a0f-b360-2c6a1fdea57b',	'接口列表',	'/rbac/interface/',	'get',	'获取接口列表'),
('8106085e-55c3-456d-a63e-2baa5baedfb4',	'用户权限',	'/rbac/user/info',	'get',	'获取用户权限'),
('81af2c6a-da9a-41f7-976b-2fb9dc497f6e',	'路由获取',	'/rbac/route/',	'get',	'获取路由列表'),
('89d1cf91-c7ea-48d0-9c93-4ed2d1f4c8bf',	'角色保存',	'/rbac/role/',	'post',	'保存角色信息'),
('92a15e56-213f-49f5-ad70-bd639a8c7d9d',	'角色删除',	'/rbac/role/',	'delete',	'删除角色信息'),
('9b0fc3ab-28d0-4241-9af4-226b2dc41cfd',	'角色批量删除',	'/rbac/role/batchdel',	'delete',	'批量删除角色信息'),
('a190d99c-4026-463b-9cf7-0b7343e881f0',	'用户修改',	'/rbac/user/editrole/',	'post',	'修改用户信息'),
('a6f4d4ae-e4f1-4e99-b1b6-43a70303feb0',	'角色信息',	'/rbac/role/:id',	'get',	'根据ID获取角色信息'),
('aded0794-f714-4b10-8cb2-54e118bd2a1f',	'用户信息',	'/rbac/user/:id',	'get',	'根据ID过去用户信息'),
('be18e4dd-4373-4157-a9dc-727b036eb4c4',	'接口批量删除',	'/rbac/interface/',	'delete',	'批量删除接口'),
('bfd8ca00-06e4-434e-b256-cb76a7b368f9',	'菜单删除',	'/rbac/menu/:id',	'delete',	'根据ID删除菜单'),
('c1ed76b8-499f-42c1-b063-e854a7798c72',	'接口绑定角色',	'/rbac/interface/relate/',	'post',	'添加或者删除角色权限【关联接口信息】'),
('c6275469-62f8-4aac-b52f-b94193552d92',	'接口删除',	'/rbac/interface/:id',	'delete',	'根据ID删除接口信息'),
('d956d997-2a91-4864-9fe5-ca0ea479ef9b',	'获取菜单',	'/rbac/menu/:id',	'get',	'根据:id获取菜单信息'),
('e4e162af-5e7b-4eaf-9512-5e6b1f86459d',	'获取菜单路径',	'/rbac/menu/1/',	'get',	'绑定路径搜索使用'),
('ed7cab17-f738-4fa4-a977-6fa016f81379',	'用户列表',	'/rbac/user/pagedlist',	'get',	'获取用户列表'),
('f0dbdc50-42ae-43bd-b63b-f51e886d8d5c',	'路由保存',	'/rbac/route/',	'post',	'保存路由信息'),
('f60012b4-1970-4b76-bf9e-a01dfaa89af3',	'菜单信息修改',	'/rbac/menu',	'post',	'修改菜单信息'),
('fed43e88-44cd-4ca6-b739-34236643f780',	'路由删除',	'/rbac/route/:id',	'delete',	'根据ID删除路由');

DROP TABLE IF EXISTS `rbac_menu`;
CREATE TABLE `rbac_menu` (
  `id` varchar(40) NOT NULL,
  `parentId` varchar(40) NOT NULL,
  `path` varchar(36) NOT NULL,
  `title` varchar(36) NOT NULL,
  `icon` varchar(36) NOT NULL,
  `permission` varchar(64) NOT NULL,
  `type` int(1) NOT NULL,
  `sort` int(3) NOT NULL,
  `isLock` tinyint(1) NOT NULL,
  `desc` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `rbac_menu` (`id`, `parentId`, `path`, `title`, `icon`, `permission`, `type`, `sort`, `isLock`, `desc`) VALUES
('3abcb3a9-9d91-4464-b3e2-e317b72e2cac',	'be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'/system/route',	'路由管理',	'share-alt-square',	'p_route_menu',	1,	2,	0,	''),
('3b9f91de-8c58-498b-83a0-ac4e3e89519c',	'be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'/system/interface',	'接口管理',	'paper-plane',	'p_interface_menu',	1,	5,	0,	''),
('4bca8eca-98be-4796-9462-2b1413732dde',	'be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'/system/menu',	'菜单管理',	'th-list',	'p_menu_menu',	1,	1,	0,	''),
('9e13f745-ca0e-4091-a23a-ebd81fdeaca3',	'be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'/system/role',	'角色管理',	'users',	'p_role_menu',	1,	3,	0,	''),
('be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'0',	'/system',	'系统管理',	'cogs',	'',	1,	10,	0,	''),
('dc3afab9-727b-49f5-9a8d-a56a1af653f0',	'be5cd580-dca8-4a6b-9a8a-b72fcb523165',	'/system/user',	'用户管理',	'user',	'p_user_menu',	1,	4,	0,	'');

DROP TABLE IF EXISTS `rbac_role`;
CREATE TABLE `rbac_role` (
  `id` varchar(40) NOT NULL,
  `name` varchar(16) NOT NULL,
  `code` varchar(64) NOT NULL,
  `isLock` tinyint(1) NOT NULL,
  `desc` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `rbac_rolefunction`;
CREATE TABLE `rbac_rolefunction` (
  `id` varchar(40) NOT NULL,
  `roleId` varchar(40) NOT NULL,
  `menuId` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_rbac_rolefunction_roleId` (`roleId`),
  KEY `ix_rbac_rolefunction_menuId` (`menuId`),
  CONSTRAINT `rbac_rolefunction_ibfk_1` FOREIGN KEY (`roleId`) REFERENCES `rbac_role` (`id`),
  CONSTRAINT `rbac_rolefunction_ibfk_2` FOREIGN KEY (`menuId`) REFERENCES `rbac_menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `rbac_roleuser`;
CREATE TABLE `rbac_roleuser` (
  `id` varchar(64) NOT NULL,
  `userId` varchar(40) NOT NULL,
  `roleId` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_rbac_roleuser_userId` (`userId`),
  KEY `ix_rbac_roleuser_roleId` (`roleId`),
  CONSTRAINT `rbac_roleuser_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `rbac_user` (`id`),
  CONSTRAINT `rbac_roleuser_ibfk_2` FOREIGN KEY (`roleId`) REFERENCES `rbac_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `rbac_route`;
CREATE TABLE `rbac_route` (
  `id` varchar(40) NOT NULL,
  `parentId` varchar(40) NOT NULL,
  `path` varchar(36) NOT NULL,
  `name` varchar(36) NOT NULL,
  `title` varchar(36) NOT NULL,
  `permission` varchar(64) NOT NULL,
  `component` varchar(36) NOT NULL,
  `componentPath` varchar(36) NOT NULL,
  `sort` int(11) NOT NULL,
  `isLock` tinyint(1) NOT NULL,
  `cache` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `rbac_route` (`id`, `parentId`, `path`, `name`, `title`, `permission`, `component`, `componentPath`, `sort`, `isLock`, `cache`) VALUES
('1524350b-152d-4af5-8436-0ff034389557',	'ac08121a-d5cb-4614-be16-289c53918b49',	'/system/menu',	'MenuPage',	'菜单管理',	'',	'menu',	'pages/sys/menu/index',	2,	0,	0),
('1ada318e-28f6-4462-8c52-c331a35848a8',	'ac08121a-d5cb-4614-be16-289c53918b49',	'/system/interface',	'InterfacePage',	'接口管理',	'',	'interface',	'',	5,	0,	1),
('2abd91a1-9a5a-4e75-94b2-e85ae6503ddc',	'ac08121a-d5cb-4614-be16-289c53918b49',	'/system/user',	'UserPage',	'用户管理',	'',	'user',	'pages/sys/user/index',	5,	0,	1),
('a907fa26-b257-4eee-b0cb-fd3ba0b8cdc4',	'ac08121a-d5cb-4614-be16-289c53918b49',	'/system/route',	'RoutePage',	'路由管理',	'',	'route',	'pages/sys/route/index',	3,	0,	1),
('ac08121a-d5cb-4614-be16-289c53918b49',	'0',	'/system',	'System',	'系统设置',	'',	'layoutHeaderAside',	'layout/header-aside/layout',	1,	0,	1),
('af4119d0-9679-4c77-a8ca-ba960549f650',	'8387b00b-20ff-4f8d-9722-6f7dec403fb5',	'/sanguo/send/mail',	'SendEmailPage',	'发送邮件',	'',	'hostadmin',	'/pages/sanguo/kefu/sendmail',	1,	0,	0),
('fa9eca1f-ee6c-4c80-ad31-9da35ccc07c7',	'ac08121a-d5cb-4614-be16-289c53918b49',	'/system/role',	'RolePage',	'角色管理',	'',	'role',	'pages/sys/role/index',	4,	0,	1);

DROP TABLE IF EXISTS `rbac_user`;
CREATE TABLE `rbac_user` (
  `id` varchar(40) NOT NULL,
  `name` varchar(64) NOT NULL,
  `realName` varchar(16) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `isLock` tinyint(1) DEFAULT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `rbac_user` (`id`, `name`, `realName`, `password`, `email`, `phone`, `isLock`, `create_at`) VALUES
('d3cd5396-923c-437f-a33f-74948f2c89df',	'superuser',	'超级管理',	'beede8811820d2f2b67acf3c252396ca',	'admin@gmail.com',	'138000',	0,	'2019-08-28 17:48:02');

-- 2019-11-14 09:49:32
