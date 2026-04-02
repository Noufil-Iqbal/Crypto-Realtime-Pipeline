-- Query 1: All coins prices
SELECT 
    coin_id,
    price_usd,
    change_24h,
    market_cap
FROM crypto_db.crypto_prices
ORDER BY price_usd DESC;

-- Query 2: Most volatile coins
SELECT
    coin_id,
    COUNT(*) as data_points,
    AVG(price_usd) as avg_price,
    MAX(price_usd) as max_price,
    MIN(price_usd) as min_price,
    AVG(ABS(change_24h)) as avg_volatility
FROM crypto_db.crypto_prices
GROUP BY coin_id
ORDER BY avg_volatility DESC;

-- Query 3: Spike detection
SELECT
    coin_id,
    timestamp,
    price_usd,
    change_24h
FROM crypto_db.crypto_prices
WHERE spike_detected = true
ORDER BY timestamp DESC;
