-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 24, 2025 at 03:01 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `heart_disease_new`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `hospital` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`id`, `name`, `mobile`, `email`, `uname`, `pass`, `hospital`, `location`, `status`) VALUES
(111, 'Dr. R.Hari Harakrish M.D', 9894442716, 'haridr@gmail.com', 'D111', '1234', 'VS Hospitals', '815/306, Poonamalle High Rd, Kilpauk, Chennai', 1),
(112, 'Dr. Avinash Jayachan M.D', 9360967387, 'ram@gmail.com', 'D112', '1234', 'Vinita Hospital', '70, Josier Street, Nungambakkam, Chennai', 1),
(113, 'Dr. D. Ashok kumar M.D', 8854512121, 'ashokmd@gmail.com', 'D113', '123456', 'Hannah Joseph Hospital', 'Vallabai Road, Chokkikulam, Madurai', 1),
(114, 'Dr. R.venkat, M.D', 8948751265, 'venkat@gmail.com', 'D114', '1234', 'Apollo', 'Trichy', 0);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(19) NOT NULL,
  `dob` varchar(15) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `guardian` varchar(20) NOT NULL,
  `gnumber` bigint(20) NOT NULL,
  `doctor` varchar(20) NOT NULL,
  `request_st` int(11) NOT NULL,
  `doc_name` varchar(20) NOT NULL,
  `doc_mobile` bigint(20) NOT NULL,
  `doc_email` varchar(40) NOT NULL,
  `doc_hospital` varchar(50) NOT NULL,
  `doc_location` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `uname`, `pass`, `address`, `city`, `guardian`, `gnumber`, `doctor`, `request_st`, `doc_name`, `doc_mobile`, `doc_email`, `doc_hospital`, `doc_location`) VALUES
(301, 'Raj', 'Male', '24-10-1998', 9360967387, 'raj@gmail.com', 'P301', '1234', '3/42, VS Nagar', 'Chennai', 'Guru', 8975645287, 'D111', 1, '', 0, '', '', ''),
(302, 'Varun', 'Male', '1999-06-05', 7895626857, 'varun@gmail.com', 'P302', '123456', '4/81, RT Nagar', 'Salem', 'Lakshmi', 7385942554, '', 0, '', 0, '', '', ''),
(303, 'Praveen', 'Male', '1991-09-08', 8956582656, 'praveen@gmail.com', 'P303', '1234', '30/2, FG Nagar', 'Tanjore', 'Raman', 7875455894, '', 0, '', 0, '', '', ''),
(304, 'Abinaya', 'Female', '2000-12-31', 9638527415, 'abi@gmail.com', 'P304', '1234', '55,hh', 'Trichy', 'Ram', 9874563214, 'D111', 1, '', 0, '', '', ''),
(305, 'Ganesh', 'Male', '1999-05-07', 9894442716, 'bgeduscanner@gmail.com', 'P305', '1234', 'GG Nagar', 'Trichy', 'Arul', 9638524568, 'D112', 0, 'Dr. R.Hari Harakrish', 9894442716, 'haridr@gmail.com', 'VS Hospitals', '815/306, Poonamalle High Rd, Kilpauk, Chennai	'),
(306, 'Dharun', 'Male', '1999-06-05', 8875614335, 'dharun@gmail.com', 'P306', '123456', '42, GS Nagar', 'Salem', 'Kumar', 9975844159, '', 0, 'Dr. R.Hari Harakrish', 9894442716, 'haridr@gmail.com', 'VS Hospitals', '815/306, Poonamalle High Rd, Kilpauk, Chennai	');

-- --------------------------------------------------------

--
-- Table structure for table `recommend`
--

CREATE TABLE `recommend` (
  `id` int(11) NOT NULL,
  `health_detail` text NOT NULL,
  `htype` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recommend`
--

INSERT INTO `recommend` (`id`, `health_detail`, `htype`) VALUES
(1, 'Lifestyle Changes (Quit smoking, healthy diet, regular exercise)', ''),
(2, 'Medications (Blood thinners, statins, beta-blockers)', ''),
(3, 'Regular Checkups', '');

-- --------------------------------------------------------

--
-- Table structure for table `recommend_food`
--

CREATE TABLE `recommend_food` (
  `id` int(11) NOT NULL,
  `food` varchar(50) NOT NULL,
  `detail` text NOT NULL,
  `ftype` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recommend_food`
--

INSERT INTO `recommend_food` (`id`, `food`, `detail`, `ftype`) VALUES
(1, 'Fruits & Vegetables', 'High in fiber, vitamins, and antioxidants', 'Healthy'),
(2, 'Whole Grains', 'Brown rice, oats, whole wheat for better heart function', 'Healthy'),
(3, 'Lean Proteins', 'Fish (salmon, tuna), skinless poultry, plant-based proteins', 'Healthy'),
(4, 'Healthy Fats', 'Avocados, nuts, olive oil for good cholesterol', 'Healthy'),
(5, 'Low-Fat Dairy', 'Skim milk, Greek yogurt for calcium without excess fat', 'Healthy'),
(6, 'Legumes & Beans', 'Rich in fiber, helps lower bad cholesterol', 'Healthy'),
(7, 'Processed & Fast Foods', 'High in trans fats & sodium', 'Avoid'),
(8, 'Red & Processed Meat', 'Leads to artery blockage', 'Avoid'),
(9, 'Sugary Drinks & Sweets', 'Increases risk of diabetes & heart disease', 'Avoid'),
(10, 'Excess Salt', 'Raises blood pressure', 'Avoid'),
(11, 'Fried Foods', 'High in unhealthy fats', 'Avoid'),
(12, 'Water', 'Best for hydration', 'Healthy'),
(13, 'Green Tea', 'Contains antioxidants', 'Healthy'),
(14, 'Beetroot Juice', 'Helps lower blood pressure', 'Healthy'),
(15, 'Low-Sodium Vegetable Juices', 'Packed with heart-friendly nutrients', 'Healthy'),
(16, 'Monitor Breathing and Pulse', 'CPR (Cardiopulmonary Resuscitation) immediately', 'First Aid'),
(17, 'Call Emergency Services Immediately', 'Dial 911 (or your local emergency number) as soon as you recognize the signs of a heart attack. ', 'First Aid'),
(18, 'Chew and Swallow Aspirin', 'Aspirin helps thin the blood and reduce the formation of blood clots that may block blood flow to the heart.', 'First Aid'),
(19, 'Monitor Breathing and Pulse', 'CPR (Cardiopulmonary Resuscitation) immediately.', 'First Aid'),
(20, 'Stay calm', 'Stay calm and keep the person as calm as possible.', 'First Aid');

-- --------------------------------------------------------

--
-- Table structure for table `suggest`
--

CREATE TABLE `suggest` (
  `id` int(11) NOT NULL,
  `pid` varchar(20) NOT NULL,
  `suggestion` varchar(100) NOT NULL,
  `prescription` varchar(100) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `doctor` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `suggest`
--

INSERT INTO `suggest` (`id`, `pid`, `suggestion`, `prescription`, `rdate`, `doctor`) VALUES
(1, 'raj', 'assasa', 'fgdfgdf', '05-04-2021', '');

-- --------------------------------------------------------

--
-- Table structure for table `test_data`
--

CREATE TABLE `test_data` (
  `id` int(11) NOT NULL,
  `patient` varchar(20) NOT NULL,
  `doctor` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `weight` double NOT NULL,
  `height` double NOT NULL,
  `blood_grp` varchar(20) NOT NULL,
  `alcohol` int(11) NOT NULL,
  `smoke` int(11) NOT NULL,
  `physical_activity` varchar(20) NOT NULL,
  `diabetes` int(11) NOT NULL,
  `hypertension` int(11) NOT NULL,
  `cholesterol` double NOT NULL,
  `resting_bp` int(11) NOT NULL,
  `heart_rate` int(11) NOT NULL,
  `family_history` int(10) NOT NULL,
  `stress_level` varchar(20) NOT NULL,
  `chest_pain` varchar(20) NOT NULL,
  `thalassemia` varchar(20) NOT NULL,
  `fasting_blood_sugar` int(11) NOT NULL,
  `ecg_results` varchar(20) NOT NULL,
  `previous_heart_problems` int(11) NOT NULL,
  `sleep_hours` int(11) NOT NULL,
  `exercise_induced_angina` int(11) NOT NULL,
  `max_heart_rate` int(11) NOT NULL,
  `temp` double NOT NULL,
  `bmi` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `test_data`
--

INSERT INTO `test_data` (`id`, `patient`, `doctor`, `name`, `age`, `gender`, `weight`, `height`, `blood_grp`, `alcohol`, `smoke`, `physical_activity`, `diabetes`, `hypertension`, `cholesterol`, `resting_bp`, `heart_rate`, `family_history`, `stress_level`, `chest_pain`, `thalassemia`, `fasting_blood_sugar`, `ecg_results`, `previous_heart_problems`, `sleep_hours`, `exercise_induced_angina`, `max_heart_rate`, `temp`, `bmi`, `status`, `date_time`) VALUES
(1, 'P305', 'D111', '', 45, '1', 58, 165, 'A+ve', 1, 1, '0', 1, 1, 285, 170, 125, 1, '0', '2', '0', 1, '0', 1, 5, 1, 24, 35, '21.30394857667585 (Healthy)', 'High', '2025-03-24 01:15:55'),
(2, 'P306', '', '', 45, '0', 58, 165, 'A+ve', 1, 1, '1', 1, 0, 265, 150, 125, 1, '0', '2', '0', 0, '1', 1, 5, 1, 24, 32, '21.30394857667585 (Healthy)', 'High', '2025-03-24 07:47:13'),
(3, 'P305', 'D112', '', 35, '1', 68, 175, 'A1+ve', 0, 1, '1', 0, 0, 161, 95, 65, 0, '0', '3', '0', 1, '0', 0, 7, 1, 162, 31, '22.20408163265306 (Healthy)', 'Moderate', '2025-03-24 07:51:13'),
(4, 'P305', 'D112', '', 35, '1', 68, 175, 'A1+ve', 0, 1, '1', 0, 0, 161, 95, 65, 0, '0', '3', '0', 1, '0', 0, 7, 1, 162, 31, '22.20408163265306 (Healthy)', 'Moderate', '2025-03-24 07:51:56'),
(5, 'P305', 'D112', '', 35, '1', 68, 175, 'A1+ve', 0, 1, '1', 0, 0, 161, 95, 65, 0, '0', '3', '0', 1, '0', 0, 7, 1, 162, 31, '22.20408163265306 (Healthy)', 'Moderate', '2025-03-24 07:52:13'),
(6, 'P305', 'D112', '', 35, '1', 68, 175, 'A1+ve', 0, 1, '1', 0, 0, 161, 95, 65, 0, '0', '3', '0', 1, '0', 0, 7, 1, 162, 31, '22.20408163265306 (Healthy)', 'Moderate', '2025-03-24 07:55:42');
