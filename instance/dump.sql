PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	user_id INTEGER NOT NULL, 
	type VARCHAR(15) NOT NULL, 
	email VARCHAR(200) NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	password VARCHAR(500) NOT NULL, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	PRIMARY KEY (user_id), 
	UNIQUE (email)
);
CREATE TABLE ingredient (
	ingredient_id INTEGER NOT NULL, 
	name TEXT NOT NULL, 
	description TEXT, 
	approver_id INTEGER, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	PRIMARY KEY (ingredient_id)
);
CREATE TABLE cuisine (
	cuisine_id INTEGER NOT NULL, 
	name TEXT NOT NULL, 
	description TEXT, 
	approver_id INTEGER, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	PRIMARY KEY (cuisine_id)
);
CREATE TABLE nutrition (
	nutrition_id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	benefits TEXT NOT NULL, 
	approver_id INTEGER, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	PRIMARY KEY (nutrition_id)
);
CREATE TABLE video (
	video_id INTEGER NOT NULL, 
	link TEXT NOT NULL, 
	PRIMARY KEY (video_id)
);
CREATE TABLE image (
	image_id INTEGER NOT NULL, 
	link TEXT NOT NULL, 
	PRIMARY KEY (image_id)
);
CREATE TABLE recipe (
	recipe_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	title TEXT NOT NULL, 
	description TEXT, 
	steps TEXT NOT NULL, 
	preparation_time VARCHAR(200) NOT NULL, 
	cooking_time VARCHAR(200) NOT NULL, 
	serving INTEGER NOT NULL, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	status VARCHAR(17) NOT NULL, 
	approver_id INTEGER, 
	PRIMARY KEY (recipe_id), 
	FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE
);
CREATE TABLE review (
	review_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	feedback TEXT, 
	created_timestamp DATE NOT NULL, 
	updated_timestamp DATE, 
	PRIMARY KEY (review_id), 
	FOREIGN KEY(user_id) REFERENCES user (user_id) ON DELETE CASCADE, 
	FOREIGN KEY(recipe_id) REFERENCES recipe (recipe_id) ON DELETE CASCADE
);
CREATE TABLE recipe_ingredient_qty (
	qty_id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	qty FLOAT NOT NULL, 
	metric VARCHAR(20) NOT NULL, 
	PRIMARY KEY (qty_id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (recipe_id) ON DELETE CASCADE, 
	FOREIGN KEY(ingredient_id) REFERENCES ingredient (ingredient_id) ON DELETE CASCADE
);
CREATE TABLE recipe_cuisine (
	id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	cuisine_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (recipe_id) ON DELETE CASCADE, 
	FOREIGN KEY(cuisine_id) REFERENCES cuisine (cuisine_id) ON DELETE CASCADE
);
CREATE TABLE recipe_nutrition (
	id INTEGER NOT NULL, 
	recipe_id INTEGER NOT NULL, 
	nutrition_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (recipe_id) ON DELETE CASCADE, 
	FOREIGN KEY(nutrition_id) REFERENCES nutrition (nutrition_id) ON DELETE CASCADE
);
COMMIT;
