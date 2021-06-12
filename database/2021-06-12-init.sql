SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;

CREATE TABLE `client` (
  `id` bigint(20) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `remote_id` bigint(20) DEFAULT NULL,
  `uid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `basicauth_password` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `connection` enum('online','offline') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `connection_change` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `resource` (
  `id` bigint(20) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `uid` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `remote_id` bigint(20) DEFAULT NULL,
  `client_id` bigint(20) DEFAULT NULL,
  `status` enum('open','closed','unknown') COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD KEY `uid` (`uid`);

ALTER TABLE `resource`
  ADD PRIMARY KEY (`id`),
  ADD KEY `uid` (`uid`);

ALTER TABLE `client`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

ALTER TABLE `resource`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;
