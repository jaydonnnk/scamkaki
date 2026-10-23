-- Slice 3: Guardian checks record the line's language and, on likely scam, the family alert status.

alter table guardian_checks
    add column language text not null default 'en' check (language in ('en', 'hi')),
    add column alert_status text check (alert_status in ('pending', 'sent', 'failed', 'off'));
