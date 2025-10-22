-- database_setup_improved.sql
-- Données avec problèmes pour mieux illustrer le traitement

CREATE DATABASE IF NOT EXISTS TP_Interface_Data;
USE TP_Interface_Data;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_utilisateur VARCHAR(50) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL
);

-- Table base1 avec données problématiques
CREATE TABLE IF NOT EXISTS base1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    age INT,
    salaire FLOAT,
    date_embauche DATE
);

-- Table base2 avec données problématiques  
CREATE TABLE IF NOT EXISTS base2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    poste VARCHAR(50),
    departement VARCHAR(50),
    salaire FLOAT
);

-- Utilisateur admin
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe)
VALUES ('admin', '$2b$12$n6uxFcUArxyCelShRyGXRu00gNBlPnFG2wNcW0MrLSzzXsbgl8O0C');

-- Données VOLONTAIREMENT désordonnées pour base1
INSERT INTO base1 (nom, age, salaire, date_embauche) VALUES
('  Ahmed ', 30, 3500, '2020-01-10'),
('sara  ', 28, NULL, '2019-05-15'),
('KARIM', 35, 4000, '2018-09-20'),
('', 32, 3800, '2021-03-25'),  -- Nom vide
('mohamed', NULL, 4200, '2017-11-30'),  -- Age manquant
('  ali  ', 29, 3300, '2017-11-10'),  -- Date manquante
('fatima', 27, 3600, '2022-06-15');

-- Données VOLONTAIREMENT désordonnées pour base2
INSERT INTO base2 (nom, poste, departement, salaire) VALUES
('Ahmed', 'ingénieur  ', '  Informatique', 3550),
('Sara', 'analyste', 'Finance', NULL),  -- Salaire manquant
('karim', NULL, 'Marketing', 4200),  -- Poste manquant
('Lina', 'Manager', '  RH  ', 4500),
('mohamed', 'dev', NULL, 3700),  -- Département manquant
('  ALI  ', 'consultant', 'Finance', 3900),
('Fatima', 'Data Scientist', 'IT', 4100);