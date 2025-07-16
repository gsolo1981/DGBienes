SELECT 
    bac.id_oc_bac,
    oc.o_ente,
    oc.aa_ocompra,
    oc.t_ocompra,
    oc.n_ocompra
FROM slu.torden_compra OC
JOIN slu.torden_compra_bac BAC 
  ON oc.id_oc_bac = bac.id_ocompra
WHERE (oc.aa_ocompra, oc.t_ocompra, oc.n_ocompra) IN (
    SELECT DISTINCT aa_ocompra, t_ocompra, n_ocompra
    FROM slu.dorden_compra_ren
    WHERE c_clase IN (990010, 560000, 790000)
      AND t_ocompra = 'OCA'
) --AND ROWNUM <= 200
;
