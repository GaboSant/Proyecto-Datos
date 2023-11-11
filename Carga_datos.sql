CREATE TABLE Ciudad(
	codigo_dane varchar(5) primary key,
	municipio varchar(40),
	departamento varchar(40)
);

CREATE TABLE Recurso(
	codigo varchar(2) primary key,
	nombre varchar(40)
);
select from Ciudad
CREATE TABLE Tiene(
	codigo_municipio varchar(5) REFERENCES Ciudad ,
	codigo_recurso varchar(2) REFERENCES Recurso,
	primary key(codigo_municipio, codigo_recurso)
);

CREATE TABLE Proyecto(
	codigo varchar(2) PRIMARY KEY,
	nombre varchar(40)
);

CREATE TABLE Explota(
	codigo_proyecto varchar(2) REFERENCES Proyecto,
	codigo_recurso varchar(2) REFERENCES Recurso,
	año integer,
	trimestre integer,
	unidad_medida varchar(15),
	tipo_contraprestacion varchar(12),
	valor_contraprestacion numeric(15,2),
	cantidad_producida numeric(12,0)
);
COPY CIUDAD(codigo_dane, municipio, departamento)
FROM 'C:\Users\felip\Desktop\Universidad\3-Semestre\Ing Datos\Proyecto\Ciudad.csv' 
DELIMITER ';'
CSV HEADER;
select *from CIUDAD

INSERT INTO Recurso VALUES('1','ARCILLAS MISCELANEAS');
INSERT INTO Recurso VALUES('2','ARENAS');
INSERT INTO Recurso VALUES('3','RECEBO');
INSERT INTO Recurso VALUES('4','GRAVAS');
INSERT INTO Recurso VALUES('5','ORO');
INSERT INTO Recurso VALUES('6','PLATA');
INSERT INTO Recurso VALUES('7','ARCILLAS CERAMICAS');
INSERT INTO Recurso VALUES('8','CARBON');
INSERT INTO Recurso VALUES('9','CALIZAS');
INSERT INTO Recurso VALUES('10','DOLOMITA');
INSERT INTO Recurso VALUES('11','SERPENTINA (SILICATO DE MAGNESIO)');
INSERT INTO Recurso VALUES('12','PLATINO');
INSERT INTO Recurso VALUES('13','ARENAS SILICEAS');
INSERT INTO Recurso VALUES('14','COBRE');
INSERT INTO Recurso VALUES('15','DIABASA');
INSERT INTO Recurso VALUES('16','MANGANESO');
INSERT INTO Recurso VALUES('17','ARCILLAS CAOLINITICA');
INSERT INTO Recurso VALUES('18','TALCO');
INSERT INTO Recurso VALUES('19','ARCILLAS FERRUGINOSAS');
INSERT INTO Recurso VALUES('20','ZINC');
INSERT INTO Recurso VALUES('21','PLOMO');
INSERT INTO Recurso VALUES('22','HIERRO');
INSERT INTO Recurso VALUES('23','PUZOLANAS');
INSERT INTO Recurso VALUES('24','ESMERALDAS');
INSERT INTO Recurso VALUES('25','ESMERALDAS SEMIPRECIOSA');
INSERT INTO Recurso VALUES('26','ESMERALDAS EN BRUTO');
INSERT INTO Recurso VALUES('27','ESMERALDAS TALLADAS');
INSERT INTO Recurso VALUES('28','MARMOL EN RAJON (RETAL DE MÁRMOL)');
INSERT INTO Recurso VALUES('29','MARMOL EN RAJÓN (RETAL DE MÁRMOL)');
INSERT INTO Recurso VALUES('30','MARMOL (BLOQUE MAYOR O IGUAL A 1 M3)');
INSERT INTO Recurso VALUES('31','MARMOL (BLOQUE MENOR A 1 M3)');
INSERT INTO Recurso VALUES('32','NIQUEL');
INSERT INTO Recurso VALUES('33','SAL');;
INSERT INTO Recurso VALUES('34','YESO');
INSERT INTO Recurso VALUES('35','FELDESPATOS');
INSERT INTO Recurso VALUES('36','CUARZO');
INSERT INTO Recurso VALUES('37','ARCILLAS BENTONITICA');

COPY Tiene(codigo_municipio, codigo_recurso)
FROM 'C:\Users\Public\Documents\Tiene.csv'
DELIMITER ';'
CSV HEADER;
select *from Tiene


INSERT INTO Proyecto VALUES('1','PRODUCTORES');
INSERT INTO Proyecto VALUES('2','MINAS PAZ DEL RIO S.A.');
INSERT INTO Proyecto VALUES('3','ACERIAS PAZ DEL RIO');
INSERT INTO Proyecto VALUES('4','Drummond - El Descanso');
INSERT INTO Proyecto VALUES('5','Drummond - La Loma');
INSERT INTO Proyecto VALUES('6','EL HATILLO CNR');
INSERT INTO Proyecto VALUES('7','Drummond - El Corozo');
INSERT INTO Proyecto VALUES('8','Cerro Matoso S.A.');
INSERT INTO Proyecto VALUES('9','BRINSA S.A.');
INSERT INTO Proyecto VALUES('10','CERREJON CONTRATO DE ASOCIACION');
INSERT INTO Proyecto VALUES('11','CERREJON  CZN - CEMT');
INSERT INTO Proyecto VALUES('12','CERREJON -  OREGANAL');
INSERT INTO Proyecto VALUES('13','CARBONES DEL CERREJON COMUNIDAD - RPP');
INSERT INTO Proyecto VALUES('14','CERREJON - PATILLA');

COPY Explota(codigo_proyecto, codigo_recurso, año, trimestre,unidad_medida, tipo_contraprestacion, valor_contraprestacion, cantidad_producida)
FROM 'C:\Users\Public\Documents\Explota.csv'
DELIMITER ';'
HEADER CSV;



