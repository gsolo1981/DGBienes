select tipodoc.codigo documento_tipo,
bienes.ente.documento,
bienes.ente.nombre,
bienes.ente.email,
bienes.ente.emailadicional,
bienes.tipo_persona.descripcion tipo_persona,
bienes.ente.fechanacimiento,
bienes.ente.sexo ,
bienes.ente.telefono,
case when bienes.ente.fecha_baja is null then 'S' else 'N' end activo,
bienes.tipo_direccion.descripcion tipo_domicilio,
bienes.direccion.calle,
bienes.direccion.piso,
bienes.direccion.dpto,
bienes.direccion.localidad,
bienes.direccion.codigo_postal
from bienes.ente
join sir.tipodocumento@fadesir tipodoc on tipodoc.id = bienes.ente.id_tipo_documento
join bienes.tipo_persona on bienes.tipo_persona.id = bienes.ente.id_tipo_persona
join bienes.direccion on bienes.direccion.id_ente  = bienes.ente.id
join bienes.tipo_direccion on bienes.tipo_direccion.id = bienes.direccion.id_tipo_direccion
order by bienes.ente.documento
