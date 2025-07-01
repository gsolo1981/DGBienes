select fade.proyecto.barrio,
fade.proyecto.ley,
fade.carterainmobiliaria.identificacion,
fade.carterainmobiliaria.circunscripcion,
fade.carterainmobiliaria.seccion,
fade.carterainmobiliaria.manzana,
fade.carterainmobiliaria.parcela,
fade.carteranucleo.descripcion division,
fade.tipo_direccion.descripcion tipo_unidad,
fade.unidadfuncional.nrounidad,
fade.unidadfuncional.partidaunidad,
fade.unidadfuncional.digitoverificador,
fade.unidadfuncional.tipoplano,
fade.unidadfuncional.valuacionfiscal,
fade.unidadfuncional.nueva,
fade.unidadfuncional.mtstotales,
fade.unidadfuncional.mtscubiertos,
case when fade.unidadfuncional.fecha_baja is null then 'S' else 'N' end habilitado
from fade.carterainmobiliaria
join fade.proyecto on fade.proyecto.id = fade.carterainmobiliaria.idproyecto
join fade.carteranucleo on fade.carteranucleo.idcarterainmobiliaria = fade.carterainmobiliaria.id
join fade.unidadfuncional on fade.unidadfuncional.idnucleo = fade.carteranucleo.id
join fade.tipo_direccion on fade.tipo_direccion.id = fade.unidadfuncional.idtipodireccion
order by fade.carterainmobiliaria.identificacion, fade.carteranucleo.descripcion, fade.unidadfuncional.nrounidad
