-- Slice 5: how the senior was contacted, the warning signs they described and whether they
-- already acted. Defaults keep checks logged before this slice valid.

alter table guardian_checks
    add column channel text not null default 'other'
        check (channel in ('call', 'sms', 'whatsapp', 'video', 'website', 'in_person', 'other')),
    add column tactics text[] not null default '{}',
    add column acted text not null default 'none'
        check (acted in ('none', 'paid', 'gave_code_or_card', 'installed_app', 'unsure'));
