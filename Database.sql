-- ۱. ساخت و انتخاب دیتابیس
CREATE DATABASE IF NOT EXISTS kitchen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kitchen_db;

-- ۲. ساخت جدول مواد اولیه (Ingredients)
CREATE TABLE ingredients (
    ing_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    unit VARCHAR(10) NOT NULL
) AUTO_INCREMENT = 1500;

-- ۳. ساخت جدول دستورات پخت (Recipes)
CREATE TABLE recipes (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    duration INT,
    category VARCHAR(20),
    recipe TEXT NOT NULL
) AUTO_INCREMENT = 6500;

-- ۴. ساخت جدول واسط (ing_needed)
CREATE TABLE ing_needed (
    food_id INT,
    ing_id INT,
    value_needed FLOAT NOT NULL,
    PRIMARY KEY (food_id, ing_id),
    
    CONSTRAINT fk_ing_needed_recipe 
        FOREIGN KEY (food_id) REFERENCES recipes(food_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
        
    CONSTRAINT fk_ing_needed_ingredient 
        FOREIGN KEY (ing_id) REFERENCES ingredients(ing_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    sub DATETIME NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT = 55500;