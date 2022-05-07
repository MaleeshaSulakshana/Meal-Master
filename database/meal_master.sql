-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 20, 2022 at 10:21 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 7.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `meal_master`
--

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int(255) NOT NULL,
  `receipt_id` int(255) NOT NULL,
  `date` date NOT NULL,
  `email` varchar(255) NOT NULL,
  `comment` varchar(2000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `receipt_id`, `date`, `email`, `comment`) VALUES
(1, 250148, '2022-04-20', 'maleesha@gmail.com', 'Good receipt.'),
(2, 250148, '2022-04-19', 'maleesha@gmail.com', 'Cool receipt for breakfast');

-- --------------------------------------------------------

--
-- Table structure for table `diet_plannings`
--

CREATE TABLE `diet_plannings` (
  `id` int(255) NOT NULL,
  `date` date NOT NULL,
  `email` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `age` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `height` varchar(255) NOT NULL,
  `weight` varchar(255) NOT NULL,
  `desired_weight` varchar(255) NOT NULL,
  `veg_or_not` varchar(100) NOT NULL,
  `preferred_foods` text NOT NULL,
  `allergies` text NOT NULL,
  `hours` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `plan` text NOT NULL,
  `couch_id` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `diet_plannings`
--

INSERT INTO `diet_plannings` (`id`, `date`, `email`, `category`, `age`, `gender`, `height`, `weight`, `desired_weight`, `veg_or_not`, `preferred_foods`, `allergies`, `hours`, `status`, `plan`, `couch_id`) VALUES
(1, '2022-04-19', 'maleesha@gmail.com', 'Healthy Life Style', '23', 'Male', '154', '65', '55', 'Non-Vegetarian', 'all', 'no', '1', 'requested', '', ''),
(2, '2022-04-20', 'maleesha@gmail.com', 'Weight Loss', '23', 'Male', '154', '65', '55', 'Non-Vegetarian', 'all', '', '1', 'requested', '', ''),
(3, '2022-04-18', 'maleesha@gmail.com', 'Weight Loss', '23', 'Male', '154', '65', '55', 'Non-Vegetarian', 'all', '', '1', 'received', 'Eat nuts', 'maleeshac@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `recipes`
--

CREATE TABLE `recipes` (
  `id` int(255) NOT NULL,
  `receipt_id` int(255) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `serves` varchar(255) NOT NULL,
  `cooking_time` varchar(255) NOT NULL,
  `prep_time` varchar(255) NOT NULL,
  `ingredients` text NOT NULL,
  `description` text NOT NULL,
  `method` text NOT NULL,
  `calories` varchar(255) NOT NULL,
  `protein` varchar(255) NOT NULL,
  `carbohydrates` varchar(255) NOT NULL,
  `total_fats` varchar(255) NOT NULL,
  `dietary_fibre` varchar(255) NOT NULL,
  `cholesterol` varchar(255) NOT NULL,
  `sodium` varchar(255) NOT NULL,
  `total_sugars` varchar(255) NOT NULL,
  `thumbnail` varchar(255) NOT NULL,
  `ingredients_image` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `recipes`
--

INSERT INTO `recipes` (`id`, `receipt_id`, `user_email`, `title`, `serves`, `cooking_time`, `prep_time`, `ingredients`, `description`, `method`, `calories`, `protein`, `carbohydrates`, `total_fats`, `dietary_fibre`, `cholesterol`, `sodium`, `total_sugars`, `thumbnail`, `ingredients_image`, `date`, `category`) VALUES
(4, 250148, 'maleesha@gmail.com', 'Baked Eggs with Swiss Chard and Green Olives', '3', '10 mins', '25 mins', '4 thick bacon slices, cut into 1-inch pieces, optional\r\n\r\n1 Tbsp Extra virgin olive oil\r\n\r\n½ small yellow onion, diced, about 1/2 cup\r\n\r\n2 garlic cloves, minced\r\n4 cups roughly chopped Swiss chard leaves, stems removed, about 1 bunch\r\n1/2 cup pitted castelvetrano olives, pitted, sliced, plus more for garnish\r\n2/3 cup heavy cream\r\n4 eggs\r\n1 Tbsp salted butter or olive oil\r\n1/4 cup panko\r\n1/4 cup crumbled feta\r\n1/2 tsp flaky salt for finishing\r\n2 Tbsp minced chives for garnishing\r\n1 loaf of crusty bread, for serving', '																																																The basic egg is elevated to ultimate luxury when baked in a wonderfully flavourful blend of cream, chard, and briny green olives. Finish with some toasted panko breadcrumbs and salty feta for a textural punch, and you\'ve got yourself a breakfast of champions. There\'s no overly sweet sugar crash or carb coma to follow, just all the flavour, heartiness, and contentment you expect from a proper breakfast. Simply serve with decent coffee and bread to sop up every last creamy dreg—brunch at home has never tasted so fantastic!\r\n											\r\n											\r\n											\r\n											', '																																																1.	Heat the oven to 425°F.\r\n\r\n2.	In a medium sized ovenproof skillet, cook the bacon over medium heat. Transfer the bacon to a paper towel lined plate. Drain off all but 1 tablespoon of the bacon grease.\r\n\r\n\r\n3.	Add 1 tablespoon of olive oil to the pan. Still over medium heat, add the onions, cooking until beginning to soften, about 5 minutes. Add the garlic and swiss chard, continuing to cook until the chard begins to wilt about 2-3 more minutes. Return the cooked bacon to the pan along with the olives. Remove from heat.\r\n\r\n4.	Create 4 wells in the chard mixture. This is where you will crack the eggs. Once all of the eggs are in the wells you created, drizzle the entire dish with the cream. Place the dish in the oven and cook for 8-10 minutes. Just until the white parts of the eggs are no longer transparent, but the egg yolks are still runny.\r\n\r\n\r\n5.	While the eggs are baking, melt the butter in a small skillet, over medium heat. Add the panko and toss to combine with the butter. Continue cooking and tossing until the panko is golden brown before removing from the heat.\r\n\r\n6.	Remove the eggs from the oven and sprinkle the toasted panko over the entire dish. Sprinkle with the feta, extra olives (if desired), flaky salt and fresh chives.\r\n\r\n\r\n7.	Serve alongside some good toasted bread.\r\n											\r\n											\r\n											\r\n											', '491', '22g', '19g', '19g', '19g', '19g', '19g', '36g', 'IMG_1495.JPG', 'IMG_1496.jpg', '2022-03-30', 'breakfast');

-- --------------------------------------------------------

--
-- Table structure for table `subscription`
--

CREATE TABLE `subscription` (
  `id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `payment_id` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subscription`
--

INSERT INTO `subscription` (`id`, `email`, `date`, `payment_id`) VALUES
(8, 'maleesha@gmail.com', '2022-04-20', 'JMDWZEAWK6FFA');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL,
  `account_type` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `psw`, `account_type`) VALUES
(1, 'Maleesha Sulakshana', 'maleesha@gmail.com', '25d55ad283aa400af464c76d713c07ad', 3),
(2, 'Maleesha', 'maleeshac@gmail.com', '25d55ad283aa400af464c76d713c07ad', 1),
(3, 'Maleesha Couch Normal', 'maleeshacn@gmail.com', '25d55ad283aa400af464c76d713c07ad', 2),
(6, 'Sulakshana', 'sulakshanac@gmail.com', '25d55ad283aa400af464c76d713c07ad', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `diet_plannings`
--
ALTER TABLE `diet_plannings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recipes`
--
ALTER TABLE `recipes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `diet_plannings`
--
ALTER TABLE `diet_plannings`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `recipes`
--
ALTER TABLE `recipes`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subscription`
--
ALTER TABLE `subscription`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
