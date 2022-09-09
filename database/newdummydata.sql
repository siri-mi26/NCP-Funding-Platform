/*
 Navicat Premium Data Transfer

 Source Server         : ncpdummydata
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 10/09/2022 03:03:27
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for campuses
-- ----------------------------
DROP TABLE IF EXISTS "campuses";
CREATE TABLE "campuses" (
  "CAMPUS_ID" text NOT NULL,
  "UNIVERSITY_ID" text,
  "CAMPUS_NAME" text,
  "CAMPUS_STATE" text,
  PRIMARY KEY ("CAMPUS_ID"),
  CONSTRAINT "UNIVERSITY_ID" FOREIGN KEY ("UNIVERSITY_ID") REFERENCES "universities" ("UNIVERSITY_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of campuses
-- ----------------------------
INSERT INTO "campuses" VALUES ('C1000', 'UWA', 'The University of Western Australia', 'WA');
INSERT INTO "campuses" VALUES ('C1002', 'UNSW', 'The University of New South Wales', 'NSW');
INSERT INTO "campuses" VALUES ('C1024', 'CUR', 'Curtin University', 'WA');
INSERT INTO "campuses" VALUES ('C1026', 'CUR', 'Kalgoorlie Campus', 'WA');
INSERT INTO "campuses" VALUES ('C1029', 'USC', 'South Bank', 'QLD');
INSERT INTO "campuses" VALUES ('C1052', 'GRIF', 'South Bank Campus - Griffith University (GU)', 'QLD');

-- ----------------------------
-- Table structure for eligibility
-- ----------------------------
DROP TABLE IF EXISTS "eligibility";
CREATE TABLE "eligibility" (
  "ELIGIBILITY_ID" TEXT(255),
  "DESCRIPTION" TEXT(255)
);

-- ----------------------------
-- Records of eligibility
-- ----------------------------
INSERT INTO "eligibility" VALUES ('1', 'Australian citizen');
INSERT INTO "eligibility" VALUES ('2', 'Obtaining credit upon completion');
INSERT INTO "eligibility" VALUES ('3', 'Undergraduate Student');
INSERT INTO "eligibility" VALUES ('4', 'Not previously Indonesian Citizen and/or Permanent Resident');
INSERT INTO "eligibility" VALUES ('5', 'Not received a short-term grant');
INSERT INTO "eligibility" VALUES ('6', 'Not received a semester grant');
INSERT INTO "eligibility" VALUES ('7', 'Born in Australia');
INSERT INTO "eligibility" VALUES (NULL, NULL);

-- ----------------------------
-- Table structure for grants
-- ----------------------------
DROP TABLE IF EXISTS "grants";
CREATE TABLE "grants" (
  "GRANT_ID" TEXT NOT NULL,
  "PROGRAM_ID" TEXT,
  "STUDENT_ID" TEXT,
  "PAYMENT_ID" TEXT,
  "UNIVERSITY_ID" TEXT,
  "CAMPUS_ID" TEXT,
  "AWARDED" TEXT(255),
  "FORMS_RECEIVED" TEXT(255),
  PRIMARY KEY ("GRANT_ID"),
  CONSTRAINT "PROGRAM_ID" FOREIGN KEY ("PROGRAM_ID") REFERENCES "programs" ("PROGRAM_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "STUDENT_ID" FOREIGN KEY ("STUDENT_ID") REFERENCES "students" ("STUDENT_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "PAYMENT_ID" FOREIGN KEY ("PAYMENT_ID") REFERENCES "payments" ("PAYMENT_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "UNIVERSITY_ID" FOREIGN KEY ("UNIVERSITY_ID") REFERENCES "universities" ("UNIVERSITY_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "CAMPUS_ID" FOREIGN KEY ("CAMPUS_ID") REFERENCES "campuses" ("CAMPUS_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of grants
-- ----------------------------
INSERT INTO "grants" VALUES ('G1000', 'P1001', 'S1000', 'A1002', 'UWA', 'C1000', 'yes', 'yes');
INSERT INTO "grants" VALUES ('G1001', 'P1004', 'S1005', 'A1001', 'UNSW', 'C1002', 'yes', 'yes');
INSERT INTO "grants" VALUES ('G1002', 'P1008', 'S1001', 'A1002', 'CUR', 'C1026', 'no', 'yes');
INSERT INTO "grants" VALUES ('G1003', 'P1007', 'S1002', 'A1003', 'CUR', 'C1024', 'no', 'no');
INSERT INTO "grants" VALUES ('G1004', 'P1015', 'S1004', 'A1004', 'UWA', 'C1000', 'yes', 'yes');
INSERT INTO "grants" VALUES ('G1005', 'P1021', 'S1005', 'A1005', 'UNSW', 'C1002', 'yes', 'yes');
INSERT INTO "grants" VALUES ('G1006', 'P1026', 'S1002', 'A1006', 'CUR', 'C1024', 'no', 'no');
INSERT INTO "grants" VALUES ('G1007', 'P1017', 'S1003', 'A1007', 'GRIF', 'C1052', 'no', 'yes');

-- ----------------------------
-- Table structure for payments
-- ----------------------------
DROP TABLE IF EXISTS "payments";
CREATE TABLE "payments" (
  "PAYMENT_ID" TEXT NOT NULL,
  "STUDENT_ID" TEXT,
  "PROGRAM_ID" text,
  "UWA_BUSINESS_UNIT" integer,
  "PAYMENT_DATE" TEXT(255),
  "PAYMENT_AMOUNT" integer,
  "UWA_ACCOUNT_NUMBER" integer,
  "FUNDING_ROUND" integer,
  "DESCRIPTION" TEXT(255),
  PRIMARY KEY ("PAYMENT_ID"),
  CONSTRAINT "STUDENT_ID" FOREIGN KEY ("STUDENT_ID") REFERENCES "students" ("STUDENT_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "PROGRAM_ID" FOREIGN KEY ("PROGRAM_ID") REFERENCES "programs" ("PROGRAM_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of payments
-- ----------------------------
INSERT INTO "payments" VALUES ('A1000', 'S1001', 'P1008', 99910, '2019-01-22', 6000, 672, 2019, 'WADE 2019 FLIP NCP GRANT');
INSERT INTO "payments" VALUES ('A1001', 'S1002', 'P1007', 99910, '2019-01-22', 1500, 672, 2018, 'DOE 2018 DSPP NCP GRANT');
INSERT INTO "payments" VALUES ('A1002', 'S1000', 'P1001', 99910, '2018-01-10', 2000, 672, 2018, 'SIMPSON 2018 ASP NCP GRANT');
INSERT INTO "payments" VALUES ('A1003', 'S1003', 'P1017', 99910, '2020-08-17', 2500, 672, 2020, 'SMITH 2020 ILSC NCP GRANT');
INSERT INTO "payments" VALUES ('A1004', 'S1005', 'P1004', 99910, '2018-01-15', 2000, 672, 2018, 'NEALE 2018 JPP NCP GRANT');
INSERT INTO "payments" VALUES ('A1005', 'S1002', 'P1026', 99910, '2021-10-18', 1500, 672, 2021, 'DOE 2021 ILSC NCP GRANT');
INSERT INTO "payments" VALUES ('A1006', 'S1004', 'P1015', 99910, '2019-08-15', 1500, 672, 2019, 'ALDAM 2019 LPP NCP GRANT');
INSERT INTO "payments" VALUES ('A1007', 'S1005', 'P1021', 99910, '2022-06-22', 1000, 672, 2020, 'NEALE 2020 FLIP NCP GRANT');

-- ----------------------------
-- Table structure for programs
-- ----------------------------
DROP TABLE IF EXISTS "programs";
CREATE TABLE "programs" (
  "PROGRAM_ID" TEXT NOT NULL,
  "PROJECT_STATUS" TEXT,
  "ELIGIBILITY_ID" TEXT,
  "PROGRAM_NAME" TEXT(255),
  "PROGRAM_ACRONYM" TEXT,
  "YEAR" integer,
  "CLASS_CODE" integer,
  "PROJECT_CODE" text,
  "ISEO_CODE" text,
  "UWA_MOBILITY_GRANT_PROJECT_GRANT_NUMBER" integer,
  "UWA_ADMIN_FUNDING_PROJECT_GRANT_NUMBER" INTEGER,
  "PROGRAM_TYPE" TEXT(255),
  "FUNDING_ACQUITTAL _DATE" TEXT,
  "PROJECT_COMPLETION_SUBMISSION_DATE" TEXT(255),
  "REFUND_UTILISATION_COMMONWEALTH_DATE" TEXT(255),
  "STATUARY_DECLORATION_DATE" TEXT(255),
  "MOBILITY_GRANT_FUNDING_RECIEVED" integer,
  "MOBILITY_GRANT_DOLLAR_SIZE" integer,
  "MOBILITY_GRANT_FUNDING_UTILISED" integer,
  "MOBILITY_GRANT_FUNDING_REMAINING" integer,
  "MOBILITY_GRANTS_RECEIVED" integer,
  "MOBILITY_GRANTS_UTILISED" integer,
  "MOBILITY_GRANTS_REMAINING" integer,
  "INTERNSHIP_GRANT_FUNDING_RECIEVED" integer,
  "INTERNSHIP_GRANT_DOLLAR_SIZE" integer,
  "INTERNSHIP_GRANT_FUNDING_UTILISED" integer,
  "INTERNSHIP_GRANT_FUNDING_REMAINING" integer,
  "INTERNSHIP_GRANTS_RECEIVED" integer,
  "INTERNSHIP_GRANTS_UTILISED" integer,
  "INTERNSHIP_GRANTS_REMAINING" integer,
  "LANGUAGE_GRANT_FUNDING_RECIEVED" integer,
  "LANGUAGE_GRANT_DOLLAR_SIZE" integer,
  "LANGUAGE_GRANT_FUNDING_UTILISED" integer,
  "LANGUAGE_GRANT_FUNDING_REMAINING" integer,
  "LANGUAGE_GRANTS_RECEIVED" integer,
  "LANGUAGE_GRANTS_UTILISED" integer,
  "LANGUAGE_GRANTS_REMAINING" integer,
  "ADMINISTRATION_GRANT_FUNDING_RECIEVED" integer,
  "ADMINISTRATION_GRANT_DOLLAR_SIZE" integer,
  "ADMINISTRATION_GRANT_FUNDING_UTILISED" integer,
  "ADMINISTRATION_GRANT_FUNDING_REMAINING" integer,
  "ADMINISTRATION_GRANTS_RECEIVED" integer,
  "ADMINISTRATION_GRANTS_UTILISED" integer,
  "ADMINISTRATION_GRANTS_REMAINING" integer,
  "TOTAL_GRANT_FUNDING_RECIEVED" integer,
  "TOTAL_GRANT_FUNDING_UTILISED" integer,
  "TOTAL_GRANT_FUNDING_REMAINING" integer,
  "TOTAL_GRANTS_RECEIVED" integer,
  "TOTAL_GRANTS_UTILISED" integer,
  "TOTAL_GRANTS_REMAINING" integer,
  PRIMARY KEY ("PROGRAM_ID"),
  CONSTRAINT "ELIGIBILITY_ID" FOREIGN KEY ("ELIGIBILITY_ID") REFERENCES "eligibility" ("ELIGIBILITY_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of programs
-- ----------------------------
INSERT INTO "programs" VALUES ('P1001', 'ONGOING', '1,3,2', 'Agriculture Semester Program', 'ASP', 2018, 902, '23902', '23902', 5011830, 5011831, 'Semester', '', '30/04/2022', '30/06/2022', '06/07/2022', 24000, 2000, 12000, 12000, 12, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9000, 1500, 7500, 1500, 6, 5, 1, 33000, 19500, 13500, 18, 11, 7);
INSERT INTO "programs" VALUES ('P1004', 'COMPLETED', '1,3,5', 'Journalism Professional Practicum', 'JPP', 2018, 700, '23700', '23700', 5011830, 5011831, 'Short Term', '', '30/04/2022', '30/06/2022', '10/07/2022', 44000, 2000, 26000, 18000, 22, 13, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 1000, 12000, 0, 12, 12, 0, 56000, 38000, 18000, 34, 25, 9);
INSERT INTO "programs" VALUES ('P1007', 'ONGOING', '1,2,3,5,6', 'Development Studies Immersion', 'DSPP', 2019, 453, '27453', '27453', 5011832, 5011833, 'Semester', '', '30/04/2023', '30/06/2023', '04/07/2023', 100000, 5000, 20000, 80000, 20, 4, 16, 18000, 1500, 13500, 4500, 12, 9, 3, 12000, 2000, 6000, 6000, 6, 3, 3, 9000, 1500, 7500, 1500, 6, 5, 1, 139000, 47000, 92000, 44, 21, 23);
INSERT INTO "programs" VALUES ('P1008', 'ONGOING', '1,2,3,4,5', 'Flexible Language Immersion', 'FLIP', 2019, 485, '27485', '27485', 5011832, 5011833, 'Semester', '', '30/04/2023', '30/06/2023', '04/07/2023', 120000, 6000, 102000, 18000, 20, 17, 3, 12000, 1000, 3000, 9000, 12, 3, 9, 0, 0, 0, 0, 0, 0, 0, 13000, 1000, 6000, 7000, 13, 6, 7, 145000, 111000, 34000, 45, 26, 19);
INSERT INTO "programs" VALUES ('P1015', 'ONGOING', '1,2,3,6', 'Law Professional Practicum', 'LPP', 2020, 500, '31500', '31500', 5011834, 5011835, 'Short Term', '', '31/12/2023', '28/02/2024', '02/03/2024', 18000, 1500, 18000, 0, 12, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17500, 1250, 17500, 0, 14, 14, 0, 35500, 35500, 0, 26, 26, 0);
INSERT INTO "programs" VALUES ('P1017', 'ONGOING', '1,2,3,4,6', 'Indonesian Language Short Course', 'ILSC', 2021, 563, '33558?', '33558?', 5011836, 5011837, 'Short Term', '', '30/04/2024', '30/06/2024', '07/07/2024', 75000, 2500, 60000, 15000, 30, 24, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12500, 1250, 8750, 3750, 10, 7, 3, 87500, 68750, 18750, 40, 31, 9);
INSERT INTO "programs" VALUES ('P1021', 'ONGOING', '1,2,3,4,6', 'Flexible Language Immersion', 'FLIP', 2022, 317, '34317', '34317', 5011838, 5011839, 'Semester', '', '30/04/2024', '30/06/2024', '03/07/2024', 14000, 1000, 10000, 4000, 14, 10, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6250, 1250, 3750, 2500, 5, 3, 2, 20250, 13750, 6500, 19, 13, 6);
INSERT INTO "programs" VALUES ('P1026', 'ONGOING', '1,2,3,4,6', 'Indonesian Language Short Course', 'ILSC', 2022, 316, '34316', '34316', 5011838, 5011839, 'Short Term', '', '30/04/2025', '30/06/2025', '04/07/2025', 12000, 1500, 10500, 1500, 8, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 2000, 8000, 4000, 6, 4, 2, 24000, 18500, 5500, 14, 11, 3);

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS "students";
CREATE TABLE "students" (
  "STUDENT_ID" text NOT NULL,
  "UNIVERSITY_ID" text,
  "CAMPUS_ID" TEXT,
  "STUDENT_NUMBER" integer,
  "TITLE" TEXT(255),
  "FIRST_NAME" TEXT(255),
  "PREFERRED_NAME" TEXT(255),
  "LAST_NAME" TEXT(255),
  "ADDRESS_LINE_1" TEXT(255),
  "ADDRESS_LINE_2" TEXT(255),
  "CITY" TEXT(255),
  "POSTCODE" integer,
  "STATE" TEXT(255),
  "COUNTRY" TEXT(255),
  "DATE_OF_BIRTH" TEXT(255),
  "PHONE_NUMBER" integer,
  "STUDENT_EMAIL" TEXT(255),
  "GENDER" TEXT(255),
  "BSB" integer,
  "ACCOUNT_NUMBER" integer,
  "FIELD_OF_STUDY" TEXT,
  "COUNTRY_OF_BIRTH" TEXT,
  "INDIGENOUS_AUSTRALIAN" TEXT(255),
  "DISABILITY" TEXT(255),
  "AUS_CITIZEN" TEXT(255),
  "NOTES" TEXT(255),
  PRIMARY KEY ("STUDENT_ID"),
  CONSTRAINT "UNIVERSITY_ID" FOREIGN KEY ("UNIVERSITY_ID") REFERENCES "universities" ("UNIVERSITY_ID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "CAMPUS_ID" FOREIGN KEY ("CAMPUS_ID") REFERENCES "campuses" ("CAMPUS_ID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO "students" VALUES ('S1000', 'UWA', 'C1000', 22344570, 'Mr', 'Homerson', 'Homer', 'Simpson', '23 Shake Drive', '', 'Yanchep', 6030, 'WA', 'Australia', '2001-07-17', 427363018, '22344570@student.uwa.edu.au', 'Male', 16343, 488368226, 'Bachelor of Commerce', 'Australia', 'null', 'null', 'yes', 'null');
INSERT INTO "students" VALUES ('S1001', 'CUR', 'C1026', 37281902, 'Mrs', 'Georgia', '', 'Wade', '39 Loose Road', '', 'Shenton Park', 6016, 'WA', 'Australia', '2000-03-12', 423829013, '37281902@student.curtin.edu.au', 'Female', 49223, 483940053, 'Bachelor of Science', 'Australia', 'null', 'no', 'yes', 'null');
INSERT INTO "students" VALUES ('S1002', 'CUR', 'C1024', 22237829, 'Mrs', 'Jane', '', 'Doe', '9 Sky Lane', '', 'Balcatta', 6002, 'WA', 'Australia', '2002-08-19', 492019219, '22237829@student.curtin.edu.au', 'Female', 38293, 462937229, 'Bachelor of Philosophy', 'England', 'yes', 'yes', 'no', 'null');
INSERT INTO "students" VALUES ('S1003', 'GRIF', 'C1052', 42890192, 'Mr ', 'John', '', 'Smith', '17 Bone Circuit', '', 'Canning Vale', 6032, 'WA', 'Australia', '2000-01-12', 420737818, '42890192@student.deakin.edu.au', 'Male', 27189, 382930272, 'Bachelor of Law', 'New Zealand', 'no', 'no', 'yes', 'null');
INSERT INTO "students" VALUES ('S1004', 'UWA', 'C1000', 27382012, 'Mrs', 'Daisy', '', 'Aldam', '23 Clever Lane', '', 'Woodlands', 6022, 'WA', 'Australia', '1998-03-27', 438929012, '27382012@student.uwa.edu.au', 'Female', 38912, 389200932, 'Bachelor of Arts', 'Australia', 'no', 'null', 'yes', 'Peanut allergy');
INSERT INTO "students" VALUES ('S1005', 'UNSW', 'C1002', 37891023, 'Mr', 'William', 'Bill', 'Neale', '45 Industry Road', '', 'Footscray', 3045, 'VIC', 'Australia', '2000-09-21', 459490203, '37891023@student.unsw.edu.au', 'Male', 48930, 482929302, 'Bachelor of Biomedical Science', 'Australia', 'null', 'no', 'yes', 'null');
INSERT INTO "students" VALUES ('S1006', 'USC', 'C1029', 45930904, 'Mr', 'Robert', 'Rob', 'Bontempelli', '16 Flag Drive', '', 'Mooloolaba', 4236, 'QLD', 'Australia', '1998-10-03', 437820102, '45930904@student.usc.edu.au', 'Male', 84920, 376483020, 'Master of Mechanical Engineering', 'Australia', 'yes', 'no', 'yes', 'Post-Graduate Student');

-- ----------------------------
-- Table structure for universities
-- ----------------------------
DROP TABLE IF EXISTS "universities";
CREATE TABLE "universities" (
  "UNIVERSITY_ID" TEXT NOT NULL,
  "UNIVERSITY_NAME" TEXT(255),
  "ABN" integer,
  "MEMBER_STATUS_2014" TEXT(255),
  "MEMBER_STATUS_2015" TEXT(255),
  "MEMBER_STATUS_2016" TEXT(255),
  "MEMBER_STATUS_2017" TEXT(255),
  "MEMBER_STATUS_2018" TEXT(255),
  "MEMBER_STATUS_2019" TEXT(255),
  "MEMBER_STATUS_2020" TEXT(255),
  "MEMBER_STATUS_2021" TEXT(255),
  "MEMBER_STATUS_2022" TEXT(255),
  "MEMBER_STATUS_2023" TEXT(255),
  "MEMBER_STATUS_2024" TEXT(255),
  "MEMBER_STATUS_2025" TEXT(255),
  "MEMBER_STATUS_2026" TEXT(255),
  "MEMBER_STATUS_2027" TEXT(255),
  "MEMBER_STATUS_2028" TEXT(255),
  "MEMBER_STATUS_2029" TEXT(255),
  "MEMBER_STATUS_2030" TEXT(255),
  PRIMARY KEY ("UNIVERSITY_ID")
);

-- ----------------------------
-- Records of universities
-- ----------------------------
INSERT INTO "universities" VALUES ('UWA', 'The University of Western Australia', 37882817280, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');
INSERT INTO "universities" VALUES ('UNSW', 'University of New South Wales', 57195873179, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');
INSERT INTO "universities" VALUES ('MACU', 'Macquarie University', 90952801237, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no');
INSERT INTO "universities" VALUES ('CUR', 'Curtin University', 99143842569, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');
INSERT INTO "universities" VALUES ('USC', 'University of the Sunshine Coast', 28441859157, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');
INSERT INTO "universities" VALUES ('GRIF', 'Griffith University', 78106094461, 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes');

PRAGMA foreign_keys = true;
