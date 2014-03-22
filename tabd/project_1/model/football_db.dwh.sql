SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `football_db` ;
CREATE SCHEMA IF NOT EXISTS `football_db` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `football_db` ;

-- -----------------------------------------------------
-- Table `football_db`.`dim_team`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `football_db`.`dim_team` ;

CREATE  TABLE IF NOT EXISTS `football_db`.`dim_team` (
  `num_team_sk` INT NOT NULL AUTO_INCREMENT ,
  `str_team` VARCHAR(255) NOT NULL ,
  `str_team_description` VARCHAR(255) NOT NULL ,
  `str_team_organization` VARCHAR(255) NOT NULL ,
  `str_country` VARCHAR(255) NOT NULL ,
  `str_association_description` VARCHAR(255) NOT NULL ,
  `str_confederation_description` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`num_team_sk`) ,
  UNIQUE INDEX `uk_dim_team_nk` (`str_team` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football_db`.`dim_competition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `football_db`.`dim_competition` ;

CREATE  TABLE IF NOT EXISTS `football_db`.`dim_competition` (
  `num_competition_sk` INT NOT NULL AUTO_INCREMENT ,
  `str_competition` VARCHAR(255) NOT NULL ,
  `str_competition_description` VARCHAR(255) NOT NULL ,
  `str_competition_title` VARCHAR(255) NOT NULL ,
  `str_competition_season` VARCHAR(255) NOT NULL ,
  `str_competition_scope` VARCHAR(255) NOT NULL ,
  `str_participant_team` VARCHAR(255) NOT NULL ,
  `str_association_description` VARCHAR(255) NOT NULL ,
  `str_confederation_description` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`num_competition_sk`) ,
  UNIQUE INDEX `uk_dim_competition_nk` (`str_competition` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football_db`.`dim_date`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `football_db`.`dim_date` ;

CREATE  TABLE IF NOT EXISTS `football_db`.`dim_date` (
  `num_date_sk` INT NOT NULL AUTO_INCREMENT ,
  `dtm_date` DATE NOT NULL ,
  `str_date_description` VARCHAR(255) NOT NULL ,
  `num_day` INT NOT NULL ,
  `str_day_of_week` VARCHAR(255) NOT NULL ,
  `num_month` INT NOT NULL ,
  `str_calendar_month` VARCHAR(255) NOT NULL ,
  `num_quarter` INT NOT NULL ,
  `num_semester` INT NOT NULL ,
  `num_year` INT NOT NULL ,
  PRIMARY KEY (`num_date_sk`) ,
  UNIQUE INDEX `uk_dim_date_nk` (`dtm_date` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football_db`.`fact_match`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `football_db`.`fact_match` ;

CREATE  TABLE IF NOT EXISTS `football_db`.`fact_match` (
  `num_match_sk` INT NOT NULL AUTO_INCREMENT ,
  `num_competition_key` INT NOT NULL ,
  `num_date_key` INT NOT NULL ,
  `num_home_team_key` INT NOT NULL ,
  `num_away_team_key` INT NOT NULL ,
  `str_match_round` VARCHAR(255) NOT NULL ,
  `num_home_team_goals` INT NOT NULL ,
  `num_away_team_goals` INT NOT NULL ,
  `str_result` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`num_match_sk`) ,
  INDEX `fk_fact_match_dim_competition_1` (`num_competition_key` ASC) ,
  INDEX `fk_fact_match_dim_date_1` (`num_date_key` ASC) ,
  INDEX `fk_fact_match_dim_team_1` (`num_home_team_key` ASC) ,
  INDEX `fk_fact_match_dim_team_2` (`num_away_team_key` ASC) ,
  INDEX `uk_match_fact_nk` (`num_competition_key` ASC, `num_home_team_key` ASC, `num_away_team_key` ASC, `str_match_round` ASC) ,
  CONSTRAINT `fk_fact_match_dim_competition_1`
    FOREIGN KEY (`num_competition_key` )
    REFERENCES `football_db`.`dim_competition` (`num_competition_sk` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_fact_match_dim_date_1`
    FOREIGN KEY (`num_date_key` )
    REFERENCES `football_db`.`dim_date` (`num_date_sk` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_fact_match_dim_team_1`
    FOREIGN KEY (`num_home_team_key` )
    REFERENCES `football_db`.`dim_team` (`num_team_sk` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_fact_match_dim_team_2`
    FOREIGN KEY (`num_away_team_key` )
    REFERENCES `football_db`.`dim_team` (`num_team_sk` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
