-- ##################################################################
-- ##### INSERARE DATE INITIALE (CU LOGIN) #####
-- ##################################################################

--- 1. LOCATIONS ---
INSERT INTO locations (room_name, building, description) VALUES
                                                             ('Room', 'Home', 'Personal room at home'),
                                                             ('Server Room', 'Home', 'Homelab closet at home');

--- 2. USERS (CU PAROLE SI ROLURI) ---
-- Adminul are toate drepturile. Userul simplu poate doar vizualiza.
INSERT INTO users (first_name, last_name, email, password, role) VALUES
                                                                     ('David', 'Bogdan', 'bogdandavid.work@gmail.com', 'admin123', 'admin'),
                                                                     ('User', 'Simplu', 'user@test.com', 'user123', 'user');

--- 3. COMPONENTS ---
INSERT INTO components (component_type, manufacturer, model_number, details) VALUES
                                                                                 ('CPU', 'AMD', 'Ryzen 5 2600', '6 Cores 12 Threads'),
                                                                                 ('RAM', 'Corsair', 'LPX 16GB DDR4 3000MHz CL16', 'Dual Channel Kit'),
                                                                                 ('SSD', 'Kingston', 'A400', '500GB SATA SSD'),
                                                                                 ('GPU', 'AMD', 'Radeon RX 5600 XT', '6GB GDDR6'),
                                                                                 ('CPU', 'Intel', 'Core i5-4460', '4 Cores 4 Threads'),
                                                                                 ('RAM', 'Patriot', 'DDR3 DIMM 8GB', '8GB DDR3'),
                                                                                 ('HDD', 'Toshiba', 'MQ01ABF050', '2.5 inch 500GB HDD 1/2'),
                                                                                 ('HDD', 'Hitachi', 'Z7K500', '2.5 inch 500GB HDD 2/2'),
                                                                                 ('CPU', 'AMD', 'Ryzen 5 5500U', '6 Cores 12 Threads'),
                                                                                 ('SSD', 'Kingston', 'NV3', '500GB M.2 NVMe SSD'),
                                                                                 ('CPU', 'Intel', 'Core i3-7100T', '2 Cores 4 Threads');

--- 4. ASSETS ---
-- Asset-urile apartin lui David (Admin) - ID 1
INSERT INTO assets (host_name, serial_number, ip_address, purchase_date, warranty_end_date, status, location_id, assigned_user_id) VALUES
                                                                                                                                       ('GAMING-PC', 'SN-DESKTOP-1', '192.168.1.100', '2020-12-20', '2022-12-20', 'Active', 1, 1),
                                                                                                                                       ('NAS-PC', 'SN-DESKTOP-2', '192.168.1.66', '2015-12-20', '2017-12-20', 'Active', 2, 1),
                                                                                                                                       ('PERSONAL-LAPTOP', 'SN-LAPTOP-67890', '192.168.1.101', '2023-11-10', '2025-11-10', 'Active', 1, 1),
                                                                                                                                       ('SERVER-PC', 'SN-DESKTOP-3', '192.168.1.99', '2019-11-10', '2021-11-10', 'Active', 2, 1);

--- 5. ASSET_COMPONENTS ---
INSERT INTO asset_components (asset_id, component_id) VALUES
                                                          (1, 1), (1, 2), (1, 3), (1, 4), -- Gaming PC
                                                          (2, 5), (2, 6), (2, 7), (2, 8), -- NAS
                                                          (3, 9), (3, 10),                -- Laptop
                                                          (4, 11), (4, 3);                -- Server

--- 6. MAINTENANCE_LOG ---
INSERT INTO maintenance_log (asset_id, date_performed, description, cost, performed_by_id) VALUES
    (2, '2025-10-02', 'TrueNAS install, thermal paste change, cleared of dust.', 0.00, 1);