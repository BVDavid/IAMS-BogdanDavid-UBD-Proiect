-- ##################################################################
-- ##### INSERT INITIAL DATA (PERSONAL INVENTORY) #####
-- ##################################################################

-- Order is  important  because of  Foreign Keys!
-- 1. locations, users, components (no dependencies)
-- 2. assets (depends on locations and users)
-- 3. asset_components (depends on assets and components)
-- 4. maintenance_log (depends on assets and users)

--- 1. LOCATIONS (Physical) ---
INSERT INTO locations (room_name, building, description) VALUES
('Room', 'Home', 'Personal room at home'),
('Server Room', 'Home', 'Homelab closet at home');


--- 2. USERS ---
INSERT INTO users (first_name, last_name, email) VALUES
('David', 'Bogdan', 'bogdandavid.work@gmail.com');

--- 3. COMPONENTS  ---
INSERT INTO components (component_type, manufacturer, model_number, details) VALUES
-------------------GAMING PC------------------------------
('CPU', 'AMD', 'Ryzen 5 2600', '6 Cores 12 Threads'),
('RAM', 'Corsair', 'LPX 16GB DDR4 3000MHz CL16', 'Dual Channel Kit'),
('SSD', 'Kingston', 'A400', '500GB SATA SSD'),
('GPU', 'AMD', 'Radeon RX 5600 XT', '6GB GDDR6'),
-------------------NAS PC------------------------------
('CPU', 'Intel', 'Core i5-4460', '4 Cores 4 Threads'),
('RAM', 'Patriot', 'DDR3 DIMM', '8GB DDR4'),
('HDD', 'Toshiba', 'MQ01ABF050', '2.5 inch 500GB HDD for NAS - 1/2'),
('HDD', 'Hitachi', 'Z7K500', '2.5 inch 500GB HDD for NAS - 2/2'),
------------------Personal Laptop-----------------------
('CPU', 'AMD', 'Ryzen 5 5500U', '6 Cores 12 Threads'),
('SSD', 'Kingston', 'NV3', '500GB M.2 NVMe SSD'),
---------------------SERVER PC----------------------------
('CPU', 'Intel', 'Core i3-7100T', '2 Cores 4 Threads');
-- it has an  SSD A400 but it's already in the table ----


--- 4. ASSETS (My equipment) ---
-- ID's being:
-- location 1 = Room, location 2 = Server Room
-- user 1 = David Bogdan
INSERT INTO assets (host_name, serial_number, ip_address, purchase_date, warranty_end_date, status, location_id, assigned_user_id) VALUES
('GAMING-PC', 'SN-DESKTOP-1', '192.168.1.100', '2020-12-20', '2022-12-20', 'Active', 1, 1),
('NAS-PC', 'SN-DESKTOP-2', '192.168.1.66', '2015-12-20', '2017-12-20', 'Active', 2, 1),
('PERSONAL-LAPTOP', 'SN-LAPTOP-67890', '192.168.1.101', '2023-11-10', '2025-11-10', 'Active', 1, 1),
('SERVER-PC', 'SN-DESKTOP-3', '192.168.1.99', '2019-11-10', '2021-11-10', 'Active', 2, 1);

--- 5. ASSET_COMPONENTS (The link between Equipment and Components) ---
-- ID's  ->  asset 1 = GAMING-PC |  asset 2 = NAS-PC | asset 3 = Personal-Lapotp | asset 4 = SERVER-PC
-- component 1-4 = Piese GAMING-PC | component 5-8 = Piese NAS-PC
INSERT INTO asset_components (asset_id, component_id) VALUES
-- GAMING-PC components (Asset 1)
(1, 1), -- (PC -> CPU AMD)
(1, 2), -- (PC -> RAM 16GB)
(1, 3), -- (PC -> SSD 500GB SATA)
(1, 4), -- (PC -> GPU RX5600XT)
-- NAS-PC components (Asset 2)
(2, 5), -- (CPU Intel)
(2, 6), -- (RAM 8GB)
(2, 7), -- (HDD 500GB 1/2)
(2, 8), -- (HDD 500GB 2/2)
-- Personal Laptop componets (Asset 3)
(3, 9), -- ( CPU AMD)
(3, 10), -- (SSD 500GB NVMe)
-- SERVER-PC components (Asset 4)
(4, 11), -- (CPU Intel)
(4, 3); -- (SSD 500GB SATA)

--- 6. MAINTENANCE_LOG ---
-- asset 2 = NAS-PC
INSERT INTO maintenance_log (asset_id, date_performed, description, cost, performed_by_id) VALUES
(2, '2025-10-02', 'TrueNAS install, thermal paste change, cleared of dust.', 0.00, 1);
