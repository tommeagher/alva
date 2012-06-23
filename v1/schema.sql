drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  subhed string not null,
  publishdate text not null,
  status not null,
  descript not null,
  private boolean DEFAULT True,
  slug string not null
);