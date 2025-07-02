-- add_row_hash_column.sql
-- Script para agregar la columna row_hash a Bienes_01_BENEFICIARIOS

USE DGBIDB;
GO

-- Verificar si la columna row_hash ya existe
IF NOT EXISTS (
    SELECT 1 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'Bienes_01_BENEFICIARIOS' 
    AND COLUMN_NAME = 'row_hash'
)
BEGIN
    -- Agregar la columna row_hash
    ALTER TABLE [dbo].[Bienes_01_BENEFICIARIOS] 
    ADD row_hash VARCHAR(64) NULL;
    
    PRINT '✅ Columna row_hash agregada exitosamente a Bienes_01_BENEFICIARIOS';
    
    -- Crear índice para mejorar performance
    CREATE INDEX IX_Bienes_01_BENEFICIARIOS_row_hash 
    ON [dbo].[Bienes_01_BENEFICIARIOS] (row_hash);
    
    PRINT '✅ Índice IX_Bienes_01_BENEFICIARIOS_row_hash creado exitosamente';
    
END
ELSE
BEGIN
    PRINT '⚠️  La columna row_hash ya existe en Bienes_01_BENEFICIARIOS';
END

-- Verificar el resultado
SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'Bienes_01_BENEFICIARIOS' 
  AND COLUMN_NAME = 'row_hash';

-- Mostrar estadísticas
SELECT 
    COUNT(*) as total_registros,
    COUNT(row_hash) as registros_con_hash,
    COUNT(*) - COUNT(row_hash) as registros_sin_hash
FROM [dbo].[Bienes_01_BENEFICIARIOS];

PRINT '🎉 Script completado. La tabla está lista para sincronización con hash.';
