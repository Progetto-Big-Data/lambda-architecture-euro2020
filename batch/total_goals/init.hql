drop table if exists old_euro_games;

create table if not exists old_euro_games(
    game_date date,
    home_team string,
    away_team string, 
    home_score int,
    away_score int,
    tournament string,
    city string,
    country string,
    neutral boolean
) row format delimited fields terminated by ',';

load data inpath 'old_fixtures.csv' overwrite into table old_euro_games;
