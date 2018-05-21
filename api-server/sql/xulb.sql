drop database if exists xulb;
create database xulb;
use xulb;

DROP TABLE IF EXISTS `group`;
CREATE TABLE `group` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
    `name` varchar(255) DEFAULT '' COMMENT 'group名称',
    PRIMARY KEY  (`id`),
    UNIQUE KEY `unq_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '组';

DROP TABLE IF EXISTS `openresty`;
CREATE TABLE `openresty` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
    `group_id` int(11) NOT NULL DEFAULT 0 COMMENT '组id',
    `host` varchar(255) DEFAULT '' COMMENT 'openresty地址',
    `port` int(6) NOT NULL DEFAULT 0 COMMENT 'openresty端口',
    PRIMARY KEY  (`id`),
    UNIQUE KEY `unq_group_id_host_port` (`group_id`,`host`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'openresty实例';

DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
    `group_id` int(11) NOT NULL DEFAULT 0 COMMENT '所属的组id',
    `name` varchar(255) NOT NULL DEFAULT '' COMMENT '项目名(对应upstream名)',
    `spec_env` varchar(255) NOT NULL DEFAULT '' COMMENT '特殊调度的环境名称，满足策略(指定uid的 调度到此环境)',
    `no_uid_env` varchar(255) NOT NULL DEFAULT '' COMMENT '无uid环境，无uid走此环境'
    `spec_uids` TEXT DEFAULT '' COMMENT '满足此uid的调度到spec_env环境',
    PRIMARY KEY  (`id`),
    UNIQUE KEY `unq_group_id_name` (`group_id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '项目';

DROP TABLE IF EXISTS `environment`;
CREATE TABLE `environment` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
    `project_id` int(11) NOT NULL DEFAULT 0 COMMENT '所属项目id',
    `name` varchar(255) NOT NULL DEFAULT '' COMMENT '环境名称',
    `uid_rate` int(4) NOT NULL DEFAULT 0 COMMENT '用户id尾数后2位的灰度比例',
    PRIMARY KEY  (`id`),
    UNIQUE KEY `unq_project_id_name` (`project_id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '环境';

DROP TABLE IF EXISTS `upstream`;
CREATE TABLE `upstream` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
    `env_id` int(11) NOT NULL DEFAULT 0 COMMENT '所属环境id',
    `host` varchar(255) DEFAULT '' COMMENT 'upstream地址',
    `port` int(6) NOT NULL DEFAULT 0 COMMENT 'upstream端口',
    PRIMARY KEY  (`id`),
    UNIQUE KEY `unq_env_id_host_port` (`env_id`,`host`,`port`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT 'upstream';