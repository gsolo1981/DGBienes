select fade2.proyecto.barrio,
fade2.proyecto.ley,
fade2.carterainmobiliaria.identificacion,
fade2.carterainmobiliaria.circunscripcion,
fade2.carterainmobiliaria.seccion,
fade2.carterainmobiliaria.manzana,
fade2.carterainmobiliaria.parcela,
fade2.carteranucleo.descripcion division,
fade2.tipo_direccion.descripcion tipo_unidad,
fade2.unidadfuncional.nrounidad,
fade2.unidadfuncional.partidaunidad,
fade2.unidadfuncional.digitoverificador,
fade2.unidadfuncional.tipoplano,
fade2.unidadfuncional.valuacionfiscal,
fade2.unidadfuncional.nueva,
fade2.unidadfuncional.mtstotales,
fade2.unidadfuncional.mtscubiertos,
case when fade2.unidadfuncional.fecha_baja is null then 'S' else 'N' end habilitado
from fade2.carterainmobiliaria
join fade2.proyecto on fade2.proyecto.id = fade2.carterainmobiliaria.idproyecto
join fade2.carteranucleo on fade2.carteranucleo.idcarterainmobiliaria = fade2.carterainmobiliaria.id
join fade2.unidadfuncional on fade2.unidadfuncional.idnucleo = fade2.carteranucleo.id
join fade2.tipo_direccion on fade2.tipo_direccion.id = fade2.unidadfuncional.idtipodireccion
order by fade2.carterainmobiliaria.identificacion, fade2.carteranucleo.descripcion, fade2.unidadfuncional.nrounidad
