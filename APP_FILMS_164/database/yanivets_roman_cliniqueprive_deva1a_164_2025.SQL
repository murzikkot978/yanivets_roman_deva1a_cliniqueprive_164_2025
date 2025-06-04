-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: MACCAUD_OLIVIER_INFO1X_FILMS_164_2023

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS yanivets_roman_cliniqueprive_deva1a_164_2025;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS yanivets_roman_cliniqueprive_deva1a_164_2025;

-- Utilisation de cette base de donnée

USE yanivets_roman_cliniqueprive_deva1a_164_2025;
-- --------------------------------------------------------

--
-- Structure de la table `t_film`
--

DROP TABLE IF EXISTS `t_consultation`;
CREATE TABLE `t_consultation` (
  `id_consultation` int NOT NULL,
  `fk_medecin` int NOT NULL,
  `fk_pationt` int NOT NULL,
  `date_consultation` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `t_facture`
--

DROP TABLE IF EXISTS `t_facture`;
CREATE TABLE `t_facture` (
  `id_facture` int NOT NULL,
  `fk_pationt` int NOT NULL,
  `montant` int NOT NULL,
  `date_emission` date NOT NULL,
  `fk_consultation` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `t_medecin`
--

DROP TABLE IF EXISTS `t_medecin`;
CREATE TABLE `t_medecin` (
  `id_medecin` int NOT NULL,
  `nom_medecin` varchar(50) NOT NULL,
  `prenome_medecin` varchar(50) NOT NULL,
  `telephone` int NOT NULL,
  `fk_specialite` int NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `t_medecin`
--

INSERT INTO `t_medecin` (`id_medecin`, `nom_medecin`, `prenome_medecin`, `telephone`, `fk_specialite`, `email`) VALUES
(1, 'testchirurg', 'Chirurg1', 1234567890, 1, '');

-- --------------------------------------------------------

--
-- Структура таблицы `t_pationt`
--

DROP TABLE IF EXISTS `t_pationt`;
CREATE TABLE `t_pationt` (
  `id_pationt` int NOT NULL,
  `nom_pationt` varchar(50) NOT NULL,
  `prenome_pationt` varchar(50) NOT NULL,
  `date_naissance` date NOT NULL,
  `adresse` varchar(50) NOT NULL,
  `telephone` int NOT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `t_pationt`
--

INSERT INTO `t_pationt` (`id_pationt`, `nom_pationt`, `prenome_pationt`, `date_naissance`, `adresse`, `telephone`, `email`) VALUES
(1, 'dima', 'Dima', '2005-03-17', 'av. lausanne 13', 222222222, 'test@gmail.com\r\n');

-- --------------------------------------------------------

--
-- Структура таблицы `t_salle`
--

DROP TABLE IF EXISTS `t_salle`;
CREATE TABLE `t_salle` (
  `id_salle` int NOT NULL,
  `salleNo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `t_salle`
--

INSERT INTO `t_salle` (`id_salle`, `salleNo`) VALUES
(1, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `t_specialite`
--

DROP TABLE IF EXISTS `t_specialite`;
CREATE TABLE `t_specialite` (
  `id_specialite` int NOT NULL,
  `nom_specialite` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `t_specialite`
--

INSERT INTO `t_specialite` (`id_specialite`, `nom_specialite`) VALUES
(1, 'Chirurg');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `t_consultation`
--
ALTER TABLE `t_consultation`
  ADD PRIMARY KEY (`id_consultation`),
  ADD KEY `id_medecin` (`fk_medecin`),
  ADD KEY `id_pationt` (`fk_pationt`);

--
-- Индексы таблицы `t_facture`
--
ALTER TABLE `t_facture`
  ADD PRIMARY KEY (`id_facture`),
  ADD KEY `id_consultation` (`fk_consultation`),
  ADD KEY `id_pationt` (`fk_pationt`);

--
-- Индексы таблицы `t_medecin`
--
ALTER TABLE `t_medecin`
  ADD PRIMARY KEY (`id_medecin`),
  ADD KEY `id_specialite` (`fk_specialite`);

--
-- Индексы таблицы `t_pationt`
--
ALTER TABLE `t_pationt`
  ADD PRIMARY KEY (`id_pationt`);

--
-- Индексы таблицы `t_salle`
--
ALTER TABLE `t_salle`
  ADD PRIMARY KEY (`id_salle`);

--
-- Индексы таблицы `t_specialite`
--
ALTER TABLE `t_specialite`
  ADD PRIMARY KEY (`id_specialite`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `t_consultation`
--
ALTER TABLE `t_consultation`
  MODIFY `id_consultation` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `t_facture`
--
ALTER TABLE `t_facture`
  MODIFY `id_facture` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `t_medecin`
--
ALTER TABLE `t_medecin`
  MODIFY `id_medecin` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `t_pationt`
--
ALTER TABLE `t_pationt`
  MODIFY `id_pationt` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `t_salle`
--
ALTER TABLE `t_salle`
  MODIFY `id_salle` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `t_specialite`
--
ALTER TABLE `t_specialite`
  MODIFY `id_specialite` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `t_consultation`
--
ALTER TABLE `t_consultation`
  ADD CONSTRAINT `consultation_ibfk_1` FOREIGN KEY (`fk_medecin`) REFERENCES `t_medecin` (`id_medecin`),
  ADD CONSTRAINT `consultation_ibfk_2` FOREIGN KEY (`fk_pationt`) REFERENCES `t_pationt` (`id_pationt`);

--
-- Ограничения внешнего ключа таблицы `t_facture`
--
ALTER TABLE `t_facture`
  ADD CONSTRAINT `facture_ibfk_1` FOREIGN KEY (`fk_consultation`) REFERENCES `t_consultation` (`id_consultation`),
  ADD CONSTRAINT `facture_ibfk_2` FOREIGN KEY (`fk_pationt`) REFERENCES `t_pationt` (`id_pationt`);

--
-- Ограничения внешнего ключа таблицы `t_medecin`
--
ALTER TABLE `t_medecin`
  ADD CONSTRAINT `medecin_ibfk_1` FOREIGN KEY (`fk_specialite`) REFERENCES `t_specialite` (`id_specialite`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
