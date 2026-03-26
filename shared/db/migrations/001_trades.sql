-- Tardigrade trade log. TPS § 1.9
CREATE TABLE IF NOT EXISTS trades (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    instrument VARCHAR(10) NOT NULL,
    direction VARCHAR(10) NOT NULL,
    entry_price DOUBLE PRECISION NOT NULL,
    target_price DOUBLE PRECISION NOT NULL,
    stop_price DOUBLE PRECISION NOT NULL,
    confluence_score DOUBLE PRECISION NOT NULL,
    confluence_breakdown JSONB,
    calendar_flags TEXT[],
    exit_price DOUBLE PRECISION,
    exit_reason VARCHAR(32),
    gross_pnl DOUBLE PRECISION,
    commission DOUBLE PRECISION,
    net_pnl DOUBLE PRECISION,
    notes TEXT
);

SELECT create_hypertable('trades', 'timestamp', if_not_exists => TRUE);
