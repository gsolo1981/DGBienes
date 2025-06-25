select tipodoc.codigo documento_tipo,
fade2.ente.documento,
fade2.ente.nombre,
fade2.ente.email,
fade2.ente.emailadicional,
fade2.tipo_persona.descripcion tipo_persona,
fade2.ente.fechanacimiento,
fade2.ente.sexo ,
fade2.ente.telefono,
case when fade2.ente.fecha_baja is null then 'S' else 'N' end activo,
fade2.tipo_direccion.descripcion tipo_domicilio,
fade2.direccion.calle,
fade2.direccion.piso,
fade2.direccion.dpto,
fade2.direccion.localidad,
fade2.direccion.codigo_postal
from fade2.ente
join sir.tipodocumento@fadesir tipodoc on tipodoc.id = fade2.ente.id_tipo_documento
join fade2.tipo_persona on fade2.tipo_persona.id = fade2.ente.id_tipo_persona
join fade2.direccion on fade2.direccion.id_ente  = fade2.ente.id
join fade2.tipo_direccion on fade2.tipo_direccion.id = fade2.direccion.id_tipo_direccion
order by fade2.ente.documento
