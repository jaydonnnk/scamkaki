-- Slice 4: what Ah Ma Bait heard (one script per Bait call) and the draft report a person reviews.

create table scripts (
    id bigint generated always as identity primary key,
    call_id bigint not null unique references calls (id),
    agency text not null,
    demand text not null,
    payee_bank text,
    payee_account text,
    paynow_id text,
    url text,
    summary text,
    created_at timestamptz not null default now()
);

create index scripts_agency_demand_created on scripts (agency, demand, created_at);

create table reports (
    id bigint generated always as identity primary key,
    call_id bigint not null unique references calls (id),
    draft text not null,
    status text not null default 'draft' check (status in ('draft', 'reviewed')),
    reviewed_at timestamptz,
    created_at timestamptz not null default now()
);
