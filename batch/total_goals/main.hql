drop view home_goals;
drop view away_goals;

create view home_goals as 
    select home_team, sum(home_score) as home_score
    from old_euro_games
    group by home_team;

create view away_goals as 
    select away_team, sum(away_score) as away_score
    from old_euro_games
    group by away_team;


select home_team, home_score + away_score as score
from home_goals join away_goals on (home_team = away_team)
sort by score desc;