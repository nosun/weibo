-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: 172.17.0.1:3306
-- Generation Time: Oct 16, 2017 at 07:06 PM
-- Server version: 5.7.10
-- PHP Version: 5.6.31-4+ubuntu16.04.1+deb.sury.org+4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `weibo_scrapy`
--

-- --------------------------------------------------------

--
-- Table structure for table `ins_user`
--

CREATE TABLE `ins_user` (
  `id` int(11) NOT NULL,
  `user_name` varchar(40) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `enable` int(11) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `wb_post`
--

CREATE TABLE `wb_post` (
  `id` int(11) NOT NULL,
  `weibo_id` varchar(200) NOT NULL,
  `weibo_uid` varchar(20) DEFAULT NULL,
  `weibo_cont` text CHARACTER SET utf8mb4,
  `weibo_img` varchar(1000) DEFAULT NULL,
  `weibo_pics` varchar(1024) DEFAULT '',
  `weibo_video` varchar(1000) DEFAULT NULL,
  `weibo_source` varchar(255) DEFAULT NULL,
  `weibo_url` varchar(300) DEFAULT NULL,
  `is_origin` int(11) DEFAULT '1',
  `is_longtext` int(11) DEFAULT '0',
  `created_at` varchar(200) DEFAULT NULL,
  `repost_num` int(11) DEFAULT '0',
  `comment_num` int(11) DEFAULT '0',
  `praise_num` int(11) DEFAULT '0',
  `device` varchar(200) DEFAULT '',
  `comment_crawled` int(11) DEFAULT '0',
  `repost_crawled` int(11) DEFAULT '0',
  `repost` text CHARACTER SET utf8mb4
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `wb_user`
--

CREATE TABLE `wb_user` (
  `id` int(11) NOT NULL,
  `uid` varchar(20) DEFAULT NULL,
  `status` int(1) DEFAULT '0',
  `name` varchar(200) DEFAULT '',
  `gender` int(11) DEFAULT '0',
  `birthday` varchar(200) DEFAULT '',
  `location` varchar(100) DEFAULT '',
  `description` varchar(500) DEFAULT '',
  `register_time` varchar(200) DEFAULT '',
  `verify_type` int(11) DEFAULT '0',
  `verify_info` varchar(2500) DEFAULT '',
  `follows_num` int(11) DEFAULT '0',
  `fans_num` int(11) DEFAULT '0',
  `wb_num` int(11) DEFAULT '0',
  `level` int(11) DEFAULT '0',
  `tags` varchar(500) DEFAULT '',
  `work_info` varchar(500) DEFAULT '',
  `contact_info` varchar(300) DEFAULT '',
  `education_info` varchar(300) DEFAULT '',
  `head_img` varchar(500) DEFAULT '',
  `search_data` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ins_user`
--
ALTER TABLE `ins_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_name` (`user_name`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `wb_post`
--
ALTER TABLE `wb_post`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `weibo_id` (`weibo_id`) USING BTREE;

--
-- Indexes for table `wb_user`
--
ALTER TABLE `wb_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`uid`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ins_user`
--
ALTER TABLE `ins_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=545;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `wb_post`
--
ALTER TABLE `wb_post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63286;
--
-- AUTO_INCREMENT for table `wb_user`
--
ALTER TABLE `wb_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1150;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
