SELECT 
    tipodoc.codigo documento_tipo, 
    TO_CHAR(fade.ente.documento) documento,           -- Convertir a texto
    fade.ente.nombre, 
    fade.ente.email, 
    fade.ente.emailadicional, 
    fade.tipo_persona.descripcion tipo_persona, 
    TO_CHAR(fade.ente.fechanacimiento, 'FMDD/FMMM/YYYY') fechanacimiento,
    fade.ente.sexo, 
    fade.ente.telefono, 
    CASE WHEN fade.ente.fecha_baja IS NULL THEN 'S' ELSE 'N' END activo, 
    fade.tipo_direccion.descripcion tipo_domicilio, 
    fade.direccion.calle, 
    fade.direccion.piso, 
    fade.direccion.dpto, 
    fade.direccion.localidad, 
    TO_CHAR(fade.direccion.codigo_postal) codigo_postal  -- Convertir a texto
FROM fade.ente 
JOIN sir.tipodocumento@fadesir tipodoc ON tipodoc.id = fade.ente.id_tipo_documento 
JOIN fade.tipo_persona ON fade.tipo_persona.id = fade.ente.id_tipo_persona 
JOIN fade.direccion ON fade.direccion.id_ente = fade.ente.id 
JOIN fade.tipo_direccion ON fade.tipo_direccion.id = fade.direccion.id_tipo_direccion 
ORDER BY fade.ente.documento;