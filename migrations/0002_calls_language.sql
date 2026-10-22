-- Slice 2: each call records which language line it came from (English or Hindi agent).

alter table calls
    add column language text not null default 'en' check (language in ('en', 'hi'));
