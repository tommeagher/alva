drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null,
  publishdate date not null,
  status not null,
  notes not null,
  private boolean DEFAULT True,
  slug string not null
);