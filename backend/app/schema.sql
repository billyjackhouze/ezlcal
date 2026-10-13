-- ezlcal schema. Safe to re-run: every statement is IF NOT EXISTS.
-- Reference tables mirror FileMaker keys so the later FM sync is a straight upsert.

CREATE TABLE IF NOT EXISTS accounts (
  id          text PRIMARY KEY,          -- CRM_accounts::z_Kp_CRMaccounts_txt (UUID text)
  name        text NOT NULL,
  types       text NOT NULL DEFAULT '',  -- C=Customer U=End user G=Engineering
  parent_id   text,                      -- z_Kf_ParentAccount
  root_id     text,                      -- z_Kf_RootParentAccount
  sales_ytd   numeric NOT NULL DEFAULT 0,
  sales_py    numeric NOT NULL DEFAULT 0,
  quotes_ytd  numeric NOT NULL DEFAULT 0,
  last_order  date,
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS contacts (
  id          text PRIMARY KEY,          -- Buyer::__Kp_Buyer
  name        text NOT NULL,
  account_id  text,                      -- Buyer::_Kf_CRMaccount_Current
  updated_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS staff (
  id          text PRIMARY KEY,          -- STA_Staff::ID_staff
  name        text NOT NULL,
  dept        text NOT NULL DEFAULT '',
  active      boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS app_users (
  username      text PRIMARY KEY,
  staff_id      text REFERENCES staff(id),
  display_name  text NOT NULL,
  pw_hash       text NOT NULL,
  must_change   boolean NOT NULL DEFAULT true,
  is_admin      boolean NOT NULL DEFAULT false,
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events (
  id            text PRIMARY KEY,        -- client-generated UUID; legacy rows keep their TODxxx id
  title         text NOT NULL,
  date          date NOT NULL,
  start_time    text NOT NULL DEFAULT '',-- 'HH:MM' or '' for all-day
  end_time      text NOT NULL DEFAULT '',
  category      text NOT NULL DEFAULT '',
  location      text NOT NULL DEFAULT '',
  notes         text NOT NULL DEFAULT '',
  deleted       boolean NOT NULL DEFAULT false,
  legacy_fm_id  text,                    -- T19_TODOLIST::id_ToDo for migrated rows
  created_by    text,
  updated_by    text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS events_updated_idx ON events (updated_at);
CREATE INDEX IF NOT EXISTS events_date_idx ON events (date);

CREATE TABLE IF NOT EXISTS event_attendees (
  event_id       text NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  attendee_type  char(1) NOT NULL CHECK (attendee_type IN ('s','a','c')),
  ref_id         text NOT NULL,
  PRIMARY KEY (event_id, attendee_type, ref_id)
);
CREATE INDEX IF NOT EXISTS event_attendees_ref_idx ON event_attendees (attendee_type, ref_id);

-- v2: admin area
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS disabled   boolean NOT NULL DEFAULT false;
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS last_login timestamptz;
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS created_by text;

-- v3: contact details, contact<->account links, offices, sync log
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS address  text NOT NULL DEFAULT '';
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS city     text NOT NULL DEFAULT '';
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS state    text NOT NULL DEFAULT '';
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS zip      text NOT NULL DEFAULT '';
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS homepage text NOT NULL DEFAULT '';
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS category text NOT NULL DEFAULT '';

ALTER TABLE contacts ADD COLUMN IF NOT EXISTS title        text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email        text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS phone_direct text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS phone_mobile text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS address      text NOT NULL DEFAULT '';   -- work address only; home address is never synced
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS city         text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS state        text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS zip          text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS linkedin     text NOT NULL DEFAULT '';
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS work_remote  boolean NOT NULL DEFAULT false;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS active       boolean NOT NULL DEFAULT true;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS last_quote   date;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS last_job     date;

CREATE TABLE IF NOT EXISTS contact_accounts (      -- mirror of CRM_BuyerAccount (FileMaker owns it)
  contact_id  text NOT NULL,
  account_id  text NOT NULL,
  sales_ytd   numeric NOT NULL DEFAULT 0,
  sales_py    numeric NOT NULL DEFAULT 0,
  quotes_ytd  numeric NOT NULL DEFAULT 0,
  PRIMARY KEY (contact_id, account_id)
);
CREATE INDEX IF NOT EXISTS contact_accounts_account_idx ON contact_accounts (account_id);

CREATE TABLE IF NOT EXISTS account_offices (
  id           text PRIMARY KEY,                  -- FileMaker __Kp_CRMaccountOffice, or a UUID for app-created
  account_id   text NOT NULL,
  office_type  text NOT NULL DEFAULT '',
  address      text NOT NULL DEFAULT '',
  city         text NOT NULL DEFAULT '',
  state        text NOT NULL DEFAULT '',
  zip          text NOT NULL DEFAULT '',
  phone        text NOT NULL DEFAULT '',
  email        text NOT NULL DEFAULT '',
  notes        text NOT NULL DEFAULT '',
  source       text NOT NULL DEFAULT 'web' CHECK (source IN ('fm','web')),
  deleted      boolean NOT NULL DEFAULT false,
  updated_by   text,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS account_offices_account_idx ON account_offices (account_id);

CREATE TABLE IF NOT EXISTS sync_runs (
  id          serial PRIMARY KEY,
  mode        text NOT NULL,
  started_at  timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz,
  ok          boolean,
  summary     jsonb
);
