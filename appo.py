
import sqlite3

conn = sqlite3.connect("Hotel management system.db")
cursor = conn.cursor()

cursor.execute("create table if not exists emp(First_Name text,Last_Name text,Gender text,id integer primary key AUTOINCREMENT ,Age real, address text, salary real)")

cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values('Mostafa', 'khalaf', 'Male', 20, 'Portsaid', 10000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('abdelrahman', 'Ali', 'Male', 25, 'Cairo', 12000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('Sara', 'Hassan', 'Female', 23, 'Alexandria', 11000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('Mona', 'ali', 'Female', 28, 'Giza', 13000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('Khaled', 'Omar', 'Male', 35, 'Luxor', 14000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('malak', 'taha', 'Female', 29, 'Aswan', 12500)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('amal', 'mohamed', 'Male', 32, 'Suez', 15000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('huda', 'qasem', 'Female', 27, 'Ismailia', 11500)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('nour', 'fadl', 'Male', 40, 'Fayoum', 16000)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('abrar', 'mahmoud', 'Female', 24, 'Tanta', 11700)")
cursor.execute("insert into emp (First_Name, Last_Name, Gender, Age, address, salary) values ('sayed', 'Fathy', 'Male', 30, 'Mansoura', 13500)")


cursor.execute("""
create table if not exists customers(
    First_Name text,
    Last_Name text,
    Customer_id integer primary key autoincrement,
    phone text,
    email text,
    Room_Price real,
    Total_Booking_Price real,
    Room_Type text,
    check_in_date date,
    check_out_date date
)
""")


cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Ahmed', 'Ali', '0101010101', 'ahmed.ali@example.com', 2000, 2200, 'single', '2024-12-01', '2024-12-05')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Mohamed', 'Hassan', '0102020202', 'mohamed.hassan@example.com', 3500, 4000, 'double', '2024-12-02', '2024-12-06')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Sara', 'Ibrahim', '0103030303', 'sara.ibrahim@example.com', 1800, 2000, 'ssingle', '2024-12-03', '2024-12-07')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Hala', 'Youssef', '0104040404', 'hala.youssef@example.com', 4000, 4400, 'double', '2024-12-04', '2024-12-08')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Khaled', 'Omar', '0105050505', 'khaled.omar@example.com', 4500, 4800, 'double', '2024-12-05', '2024-12-09')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Mona', 'Adel', '0106060606', 'mona.adel@example.com', 3000, 3300, 'double', '2024-12-06', '2024-12-10')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Eman', 'Salah', '0107070707', 'eman.salah@example.com', 2200, 2500, 'single', '2024-12-07', '2024-12-11')")
cursor.execute("insert into customers (First_Name, Last_Name, phone, email, Room_Price, Total_Booking_Price, Room_Type, check_in_date, check_out_date) values('Tamer', 'Mahmoud', '0108080808', 'tamer.mahmoud@example.com', 2700, 3100, 'single', '2024-12-08', '2024-12-12')")







cursor.execute("create table if not exists rooms(room_id integer primary key AUTOINCREMENT ,room_type text, price real,availability boolean,floor integer)")

cursor.execute("insert into rooms (room_type, price, availability, floor) values('single', 3000, 'true',1)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('double', 3450, 'false',1)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('single', 2000, 'false',2)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('single', 2500, 'true',2)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('double', 4000, 'false',4)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('double', 3200, 'true',3)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('double', 2400, 'false',5)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('single', 3100, 'true',6)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('double', 3400, 'false',7)"),
cursor.execute("insert into rooms (room_type, price, availability, floor) values('single', 29000, 'true',8)"),







cursor.execute("create table if not exists booking(customer_id integer not null,room_id integer not null,check_in_date date not null,check_out_date date not null,total_price real not null,created_at timestamp default current_timestamp,foreign key (customer_id) references customers(id),foreign key (room_id) references rooms(room_id))")

cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (1, 101, '2022-2-01', '2022-12-05', 12000.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (2, 102, '2023-1-10', '2023-12-15',  2300.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (3, 103, '2024-3-13', '2024-5-15',  12300.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (4, 104, '2024-8-10', '2024-12-15',  121000.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (5, 105, '2024-4-6', '2024-11-5',  37000.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (6, 106, '2021-12-7', '2021-12-15',  85000.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (7, 107, '2023-10-10', '2023-10-24',  36000.0)")
cursor.execute("INSERT INTO booking (customer_id, room_id, check_in_date, check_out_date,total_price) VALUES (8, 108, '2024-5-10', '2024-10-15',  31000.0)")


















conn.commit()

conn.close()










































































