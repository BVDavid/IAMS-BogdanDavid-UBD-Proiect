-- stops the  verification of foreign keys temporarly to be able to delete them in order
SET session_replication_role = 'origin';

-- delete existing tables (to be able to run the  script multiple times for testing)
DROP TABLE IF EXISTS asset_components;
DROP TABLE IF EXISTS maintenance_log;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS components;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS locations;

-- Start the verification of foreign keys
SET session_replication_role = 'origin';

--- TABELA 1: LOCATIONS (physical) ---
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    building VARCHAR(100),
    description TEXT
);

--- TABEL 2: USERS  ---
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20)
);

--- TABEL 3: COMPONENTS (Component types: RAM, CPU, SSD, etc.) ---
CREATE TABLE components (
    component_id SERIAL PRIMARY KEY,
    component_type VARCHAR(50) NOT NULL, -- Ex: 'CPU', 'RAM', 'SSD', 'GPU'
    manufacturer VARCHAR(50),
    model_number VARCHAR(100) NOT NULL,
    details VARCHAR(50), -- Ex: '16GB', '1TB', 'Ryzen 7'
    UNIQUE (component_type, model_number)
);

--- TABEL 4: ASSETS (Main equipemnt: PCs, Laptops) ---
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    host_name VARCHAR(100) UNIQUE NOT NULL,
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    ip_address VARCHAR(15),
    purchase_date DATE,
    warranty_end_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Activ', -- Ex: 'Active', 'In repair', 'Retired'
    
    location_id INTEGER REFERENCES locations(location_id) ON DELETE SET NULL,
    assigned_user_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL
);

--- TABEL 5: ASSET_COMPONENTS (N:M) ---
-- Ties components to equipment (a PC has many componente, a component can be (used) in multiple PCs)
CREATE TABLE asset_components (
    asset_component_id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(asset_id) ON DELETE CASCADE,
    component_id INTEGER REFERENCES components(component_id) ON DELETE RESTRICT,
    UNIQUE (asset_id, component_id)
);

--- TABELA 6: MAINTENANCE_LOG  ---
CREATE TABLE maintenance_log (
    log_id SERIAL PRIMARY KEY,
    asset_id INTEGER REFERENCES assets(asset_id) ON DELETE CASCADE NOT NULL,
    date_performed DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT NOT NULL,
    cost DECIMAL(10, 2),
    performed_by_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL
);
