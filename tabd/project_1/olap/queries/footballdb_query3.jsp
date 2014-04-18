<%@ page session="true" contentType="text/html; charset=ISO-8859-1" %>
<%@ taglib uri="http://www.tonbeller.com/jpivot" prefix="jp" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jstl/core" %>

<jp:mondrianQuery id="query01" 
	jdbcDriver="com.mysql.jdbc.Driver" 
	jdbcUrl="jdbc:mysql://localhost/football_db?user=root&password=root" 
	catalogUri="/WEB-INF/queries/FootballDB.xml">
WITH 
    MEMBER [Measures].[Goles R] AS 
    [Measures].[HomeTeamGoals]
    
    MEMBER [Measures].[Goles A] AS 
    [Measures].[AwayTeamGoals]
    
    MEMBER [Measures].[Derrotas] AS 
    STR(INT(ROUND([Measures].[HomeWins],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerHomeWins].Value, 1)))||"%)"
    
    MEMBER [Measures].[Victorias] AS 
    STR(INT(ROUND([Measures].[Awaywins],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerAwayWins].Value, 1)))||"%)"
    
    MEMBER [Measures].[Empates] AS 
    STR(INT(ROUND([Measures].[Draws],0)))||" ("||LTRIM(STR(ROUND([Measures].[PerDraws].Value, 1)))||"%)"

    MEMBER [Measures].[Puntos Obtenidos] AS
    (INT(ROUND([Measures].[AwayWins],0))*3 + INT(ROUND([Measures].[Draws],0))*1)
    
    MEMBER [Measures].[Rendimiento] AS
    INT(ROUND(([Measures].[Puntos Obtenidos] / ([Measures].[Matchs]*3)) * 100,2))
    
    MEMBER [Measures].[Puntos] AS
    LTRIM(STR(INT([Measures].[Puntos Obtenidos])))||" ("||LTRIM(STR([Measures].[Rendimiento]))||"%)"
    
    MEMBER [Measures].[Media R] AS
    ROUND([Measures].[HomeTeamGoals] / [Measures].[Matchs], 1)
    
    MEMBER [Measures].[Media A] AS
    ROUND([Measures].[AwayTeamGoals] / [Measures].[Matchs], 1)
    
    MEMBER [Measures].[U Victoria] AS
    [Measures].[LastLost]
    
    MEMBER [Measures].[U Derrota] AS
    [Measures].[LastWin]
SELECT
    {
        [Measures].[Matchs], [Measures].[Puntos],
        [Measures].[Victorias], [Measures].[U Victoria],
        [Measures].[Derrotas], [Measures].[U Derrota],
        [Measures].[Empates], [Measures].[LastDraw],
        [Measures].[Goles A], [Measures].[Media A], 
        [Measures].[Goles R], [Measures].[Media R]
    } ON COLUMNS, 
    NON EMPTY{(
        [Competition], [AwayTeam], [Date]
    )} ON ROWS
FROM Matchs
</jp:mondrianQuery>

<c:set var="title01" scope="session">Football DB's Cube - Away Team's Performance</c:set>
