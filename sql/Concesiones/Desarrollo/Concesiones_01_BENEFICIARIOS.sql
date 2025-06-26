SELECT 
    tipodoc.codigo documento_tipo, 
    TO_CHAR(fade2.ente.documento) documento,           -- Convertir a texto
    fade2.ente.nombre, 
    fade2.ente.email, 
    fade2.ente.emailadicional, 
    fade2.tipo_persona.descripcion tipo_persona, 
    TO_CHAR(fade2.ente.fechanacimiento, 'FMDD/FMMM/YYYY') fechanacimiento,
    fade2.ente.sexo, 
    fade2.ente.telefono, 
    CASE WHEN fade2.ente.fecha_baja IS NULL THEN 'S' ELSE 'N' END activo, 
    fade2.tipo_direccion.descripcion tipo_domicilio, 
    fade2.direccion.calle, 
    fade2.direccion.piso, 
    fade2.direccion.dpto, 
    fade2.direccion.localidad, 
    TO_CHAR(fade2.direccion.codigo_postal) codigo_postal  -- Convertir a texto
FROM fade2.ente 
JOIN sir.tipodocumento@fade2sir tipodoc ON tipodoc.id = fade2.ente.id_tipo_documento 
JOIN fade2.tipo_persona ON fade2.tipo_persona.id = fade2.ente.id_tipo_persona 
JOIN fade2.direccion ON fade2.direccion.id_ente = fade2.ente.id 
JOIN fade2.tipo_direccion ON fade2.tipo_direccion.id = fade2.direccion.id_tipo_direccion 
ORDER BY fade2.ente.documento;