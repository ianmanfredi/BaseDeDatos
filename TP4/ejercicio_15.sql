
CREATE TABLE IF NOT EXISTS Accesos (
    AccesoId INTEGER PRIMARY KEY AUTOINCREMENT,
    UsuarioId INTEGER NOT NULL,
    FechaAcceso DATETIME NOT NULL,
    DireccionIP VARCHAR(45) NOT NULL
);

CREATE TABLE IF NOT EXISTS AuditoriaAccesos (
    AuditoriaId INTEGER PRIMARY KEY AUTOINCREMENT,
    UsuarioId INTEGER NOT NULL,
    FechaAcceso DATETIME NOT NULL,
    DireccionIP VARCHAR(45) NOT NULL,
    EstadoAcceso VARCHAR(20) NOT NULL
);

CREATE VIEW IF NOT EXISTS AccesosSospechosos AS
SELECT 
    a.AccesoId,
    a.UsuarioId,
    a.FechaAcceso,
    a.DireccionIP,
    (
        SELECT COUNT(*) 
        FROM Accesos b 
        WHERE b.DireccionIP = a.DireccionIP 
        AND b.FechaAcceso >= datetime(a.FechaAcceso, '-24 hours')
    ) as intentos_24h
FROM Accesos a;

CREATE TRIGGER IF NOT EXISTS TR_AuditarAccesos
AFTER INSERT ON Accesos
BEGIN
    INSERT INTO AuditoriaAccesos (UsuarioId, FechaAcceso, DireccionIP, EstadoAcceso)
    SELECT 
        NEW.UsuarioId,
        NEW.FechaAcceso,
        NEW.DireccionIP,
        CASE 
            WHEN (SELECT COUNT(*) 
                  FROM Accesos 
                  WHERE DireccionIP = NEW.DireccionIP 
                  AND FechaAcceso >= datetime('now', '-24 hours')) > 3 
            THEN 'Fallido'
            ELSE 'Exitoso'
        END;
END;

INSERT INTO Accesos (UsuarioId, FechaAcceso, DireccionIP) VALUES 
(1, datetime('now'), '192.168.1.100'),
(2, datetime('now', '-1 hour'), '192.168.1.101'),
(3, datetime('now', '-2 hours'), '192.168.1.102');

INSERT INTO Accesos (UsuarioId, FechaAcceso, DireccionIP) VALUES 
(4, datetime('now'), '192.168.1.200'),
(4, datetime('now', '-5 minutes'), '192.168.1.200'),
(4, datetime('now', '-10 minutes'), '192.168.1.200'),
(4, datetime('now', '-15 minutes'), '192.168.1.200');

INSERT INTO Accesos (UsuarioId, FechaAcceso, DireccionIP) VALUES 
(5, datetime('now', '-12 hours'), '192.168.1.300'),
(5, datetime('now', '-6 hours'), '192.168.1.300'),
(6, datetime('now', '-18 hours'), '192.168.1.301');

SELECT * FROM AuditoriaAccesos;

SELECT * FROM AccesosSospechosos WHERE intentos_24h > 3;

SELECT 
    DireccionIP,
    COUNT(*) as total_accesos,
    MAX(FechaAcceso) as ultimo_acceso
FROM Accesos
GROUP BY DireccionIP;