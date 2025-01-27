DROP DATABASE IF EXISTS woprchatapp;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE woprchatapp;
USE woprchatapp;

GRANT ALL PRIVILEGES ON woprchatapp.* TO 'testuser';

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    delete_flag BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE distinction_types (
    distinction_type_id INT AUTO_INCREMENT PRIMARY KEY,
    distinction_type_name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    channel_name VARCHAR(255) UNIQUE NOT NULL,
    distinction_type_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (distinction_type_id) REFERENCES distinction_types(distinction_type_id) ON DELETE CASCADE
);

CREATE TABLE fixed_messages (
    fixed_message_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT,
    distinction_type_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (distinction_type_id) REFERENCES distinction_types(distinction_type_id) ON DELETE CASCADE
);

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    channel_id INT NOT NULL,
    message TEXT,
    fixed_message_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON DELETE CASCADE,
    FOREIGN KEY (fixed_message_id) REFERENCES fixed_messages(fixed_message_id) ON DELETE CASCADE
);

INSERT INTO users(user_name, email, password, is_admin, delete_flag) VALUES('管理者','admin@gmail.com','713bfda78870bf9d1b261f565286f85e97ee614efe5f0faf7c34e7ca4f65baca', 1, 0);
INSERT INTO users(user_name, email, password, is_admin, delete_flag) VALUES('テスト','test@gmail.com','d55f661526b004d3a9cc4e7bc9542fc624da3784285b262960cd4605324e03e5', 0, 0);
INSERT INTO distinction_types(distinction_type_name) VALUES('ビジネス');
INSERT INTO distinction_types(distinction_type_name) VALUES('プライベート');
INSERT INTO channels(user_id, channel_name, distinction_type_id) VALUES(1, '仕事部屋', 1);
INSERT INTO channels(user_id, channel_name, distinction_type_id) VALUES(1, 'ぼっち部屋', 2);
INSERT INTO fixed_messages(message, distinction_type_id) VALUES('了解しました。', 1);
INSERT INTO fixed_messages(message, distinction_type_id) VALUES('少々お待ちください。', 1);
INSERT INTO fixed_messages(message, distinction_type_id) VALUES('確認お願いします。', 1);
INSERT INTO messages(user_id, channel_id, message, fixed_message_id) VALUES(1, 1, '教えて〜', 1);
INSERT INTO messages(user_id, channel_id, message, fixed_message_id) VALUES(1, 1, '誰かかまって〜', 2);