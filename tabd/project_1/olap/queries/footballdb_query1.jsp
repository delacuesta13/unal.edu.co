<%@ page session="true" contentType="text/html; charset=ISO-8859-1" %>
<%@ taglib uri="http://www.tonbeller.com/jpivot" prefix="jp" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jstl/core" %>

<jp:mondrianQuery id="query01" 
	jdbcDriver="com.mysql.jdbc.Driver" 
	jdbcUrl="jdbc:mysql://localhost/football_db?user=root&password=root" 
	catalogUri="/WEB-INF/queries/FootballDB.xml">
WITH 
    MEMBER [Measures].[Victorias Locales] AS 
    STR(INT(ROUND([Measures].[HomeWins],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerHomeWins].Value, 1)))||"%)"
    
    MEMBER [Measures].[Victorias Visitantes] AS 
    STR(INT(ROUND([Measures].[Awaywins],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerAwayWins].Value, 1)))||"%)"
    
    MEMBER [Measures].[Empates] AS 
    STR(INT(ROUND([Measures].[Draws],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerDraws].Value, 1)))||"%)"
SELECT
    {
        [Measures].[Matchs], [Measures].[FirstPlayedMatch], [Measures].[LastPlayedMatch],
        [Measures].[Goals], [Measures].[GoalsAverage],
        [Measures].[HomeTeamGoals], [Measures].[AwayTeamGoals],
        [Measures].[Victorias Locales], [Measures].[Victorias Visitantes], [Measures].[Empates]
    } ON COLUMNS,
    {(
        [Competition], [Date]
    )} ON ROWS
FROM Matchs
</jp:mondrianQuery>

<c:set var="title01" scope="session">Football DB's Cube - Overview</c:set>
