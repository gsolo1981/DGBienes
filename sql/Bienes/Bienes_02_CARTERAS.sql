select bienes.proyecto.barrio,
bienes.proyecto.ley,
bienes.carterainmobiliaria.identificacion,
bienes.carterainmobiliaria.circunscripcion,
bienes.carterainmobiliaria.seccion,
bienes.carterainmobiliaria.manzana,
bienes.carterainmobiliaria.parcela,
bienes.carteranucleo.descripcion division,
bienes.tipo_direccion.descripcion tipo_unidad,
bienes.unidadfuncional.nrounidad,
bienes.unidadfuncional.piso,
bienes.unidadfuncional.depto,
bienes.unidadfuncional.telefono,
bienes.unidadfuncional.partidaunidad,
bienes.unidadfuncional.digitoverificador,
bienes.unidadfuncional.tipoplano,
bienes.unidadfuncional.valuacionfiscal,
bienes.unidadfuncional.nueva,
bienes.unidadfuncional.mtstotales,
bienes.unidadfuncional.mtscubiertos,
case when bienes.unidadfuncional.fecha_baja is null then 'S' else 'N' end habilitado
from bienes.carterainmobiliaria
join bienes.proyecto on bienes.proyecto.id = bienes.carterainmobiliaria.idproyecto
join bienes.carteranucleo on bienes.carteranucleo.idcarterainmobiliaria = bienes.carterainmobiliaria.id
join bienes.unidadfuncional on bienes.unidadfuncional.idnucleo = bienes.carteranucleo.id
join bienes.tipo_direccion on bienes.tipo_direccion.id = bienes.unidadfuncional.idtipodireccion
order by bienes.carterainmobiliaria.identificacion, bienes.carteranucleo.descripcion, bienes.unidadfuncional.nrounidad
