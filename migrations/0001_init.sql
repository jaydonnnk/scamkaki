-- Slice 1: calls stored from Bolna webhooks, and Guardian tool checks.
-- scripts and reports tables arrive with Slice 4.

create table calls (
    id bigint generated always as identity primary key,
    execution_id text not null unique,
    line text not null check (line in ('bait', 'guardian')),
    fixture_case text,
    transcript text not null default '',
    extracted jsonb not null default '{}'::jsonb,
    leaks jsonb not null default '[]'::jsonb,
    status text not null,
    duration_s integer,
    created_at timestamptz not null default now()
);

create table guardian_checks (
    id bigint generated always as identity primary key,
    execution_id text,
    agency text not null,
    demand text not null,
    verdict text not null check (verdict in ('likely_scam', 'unclear', 'no_scam_signs')),
    similar_count integer not null,
    created_at timestamptz not null default now()
);
