-- Keep a log of any SQL queries you execute as you solve the mystery.

--To get more info about the incidence
SELECT * FROM crime_scene_reports WHERE street = "Chamberlin Street" AND description LIKE "%theft%";

-- Finding more info from witnesses
SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28;
SELECT * FROM interviews WHERE id = 161 OR id = 162 OR id = 163;

-- Searching for people who exit from courthouse within 10 minute of incidence
SELECT license_plate, id FROM people WHERE license_plate IN
(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25);

-- Checking atm history of 28/07/2021 of people who exit from couthouse within 10 minute of incidence 
SELECT person_id, account_number FROM bank_accounts
WHERE person_id IN (SELECT id FROM people WHERE license_plate IN
(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25));


SELECT * FROM atm_transactions WHERE account_number IN
(SELECT account_number FROM bank_accounts
WHERE person_id IN (SELECT id FROM people WHERE license_plate IN
(SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25))) 
AND year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street";

SELECT account_number, person_id FROM bank_accounts WHERE
account_number = 49610011 OR account_number = 28500762 OR account_number = 25506511 OR account_number = 26013199;
person_id | account_number
686048 | 49610011
467400 | 28500762
396669 | 25506511
514354 | 26013199

SELECT id, passport_number FROM people
WHERE id = 686048 OR id = 467400 OR id = 396669 OR id = 514354;
id | passport_number
396669 | 7049073643
467400 | 8496433585 --this one
514354 | 3592750733
686048 | 5773159633 --this one

SELECT * FROM flights WHERE
origin_airport_id = 8 AND year = 2020 AND month = 7 AND day = 29
ORDER BY hour LIMIT 1;
id | origin_airport_id | destination_airport_id | year | month | day | hour | minute
36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20--THE EARLIEST FLIGHT OUT FROM Fiftyville on 29

SELECT * FROM airports WHERE id = 4;
id | abbreviation | full_name | city
4 | LHR | Heathrow Airport | London --thief ESCAPED TO

SELECT * FROM passengers
WHERE flight_id = 36;
flight_id | passport_number | seat
36 | 7214083635 | 2A
36 | 1695452385 | 3B
36 | 5773159633 | 4A
36 | 1540955065 | 5C
36 | 8294398571 | 6C
36 | 1988161715 | 6D
36 | 9878712108 | 7A
36 | 8496433585 | 7B

SELECT id, phone_number FROM people WHERE
id = 467400 OR id = 686048;
id | phone_number
467400 | (389) 555-5198
686048 | (367) 555-5533

SELECT * FROM phone_calls WHERE
(caller = "(389) 555-5198" OR caller = "(367) 555-5533")
AND year = 2020 AND month = 7 AND day = 28;
id | caller | receiver | year | month | day | duration
233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
236 | (367) 555-5533 | (344) 555-9601 | 2020 | 7 | 28 | 120
245 | (367) 555-5533 | (022) 555-4052 | 2020 | 7 | 28 | 241
285 | (367) 555-5533 | (704) 555-5790 | 2020 | 7 | 28 | 75

SELECT name FROM people
WHERE phone_number = "(367) 555-5533";
name
Ernest--THE THIEF

SELECT name FROM people
WHERE phone_number = "(375) 555-8161";
name
Berthold--THE ACCOMPLIANCE