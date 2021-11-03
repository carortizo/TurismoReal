CREATE TABLE acompañantes (
    rut                   INTEGER NOT NULL,
    nombre                VARCHAR2(75) NOT NULL,
    reservas_id_reservas  INTEGER NOT NULL
);

ALTER TABLE acompañantes ADD CONSTRAINT acompañantes_pk PRIMARY KEY ( rut );

CREATE TABLE check_in (
    id_check_in                INTEGER NOT NULL,
    descripcion                VARCHAR2(75) NOT NULL,
    registro_pago_id_reg_pago  INTEGER NOT NULL,
    personal_id_personal       INTEGER NOT NULL
);

CREATE INDEX check_in__idx ON
    check_in (
        registro_pago_id_reg_pago
    ASC );

ALTER TABLE check_in ADD CONSTRAINT check_in_pk PRIMARY KEY ( id_check_in );

CREATE TABLE check_out (
    id_check_out                    INTEGER NOT NULL,
    descripcion                     VARCHAR2(75) NOT NULL,
    multa                           INTEGER NOT NULL,
    registro_arri_id_registro_arri  INTEGER NOT NULL,
    personal_id_personal            INTEGER NOT NULL
);

CREATE INDEX check_out__idx ON
    check_out (
        registro_arri_id_registro_arri
    ASC );

ALTER TABLE check_out ADD CONSTRAINT check_out_pk PRIMARY KEY ( id_check_out );

CREATE TABLE cliente (
    rut         INTEGER NOT NULL,
    nombre      VARCHAR2(75) NOT NULL,
    apellidos   VARCHAR2(75) NOT NULL,
    telefono    INTEGER NOT NULL,
    correo      VARCHAR2(75) NOT NULL,
    contraseña  VARCHAR2(75) NOT NULL
);

ALTER TABLE cliente ADD CONSTRAINT cliente_pk PRIMARY KEY ( rut );

CREATE TABLE departamento (
    id_depto                  INTEGER NOT NULL,
    metros_cua                INTEGER NOT NULL,
    direccion                 VARCHAR2(75) NOT NULL,
    descripcion               VARCHAR2(75) NOT NULL,
    precio                    INTEGER NOT NULL,
    img                       BLOB,
    zonas_id_zonas            INTEGER NOT NULL,
    inventario_id_inventario  INTEGER NOT NULL,
    std_depto_id_stdo_depto   INTEGER NOT NULL
);

ALTER TABLE departamento ADD CONSTRAINT departamento_pk PRIMARY KEY ( id_depto );

CREATE TABLE inventario (
    id_inventario  INTEGER NOT NULL,
    habitacion     INTEGER NOT NULL,
    camas          VARCHAR2(75) NOT NULL,
    incluido       VARCHAR2(255) NOT NULL,
    baños          INTEGER NOT NULL
);

ALTER TABLE inventario ADD CONSTRAINT inventario_pk PRIMARY KEY ( id_inventario );

CREATE TABLE metodo_pago (
    id_met_pago  INTEGER NOT NULL,
    descripcion  VARCHAR2(50) NOT NULL
);

ALTER TABLE metodo_pago ADD CONSTRAINT metodo_pago_pk PRIMARY KEY ( id_met_pago );

CREATE TABLE personal (
    id_personal                INTEGER NOT NULL,
    nombre                     VARCHAR2(75) NOT NULL,
    apellidos                  VARCHAR2(75) NOT NULL,
    rut                        INTEGER NOT NULL,
    telefono                   INTEGER NOT NULL,
    correo                     VARCHAR2(75) NOT NULL,
    contraseña                 VARCHAR2(75) NOT NULL,
    tipo_personal_id_tipo_prs  INTEGER NOT NULL,
    zonas_id_zonas             INTEGER NOT NULL
);

ALTER TABLE personal ADD CONSTRAINT personal_pk PRIMARY KEY ( id_personal );

CREATE TABLE registro_arri (
    id_registro_arri      INTEGER NOT NULL,
    descripcion           VARCHAR2(75) NOT NULL,
    pago_total            VARCHAR2(75) NOT NULL,
    check_in_id_check_in  INTEGER NOT NULL
);

CREATE INDEX registro_arri__idx ON
    registro_arri (
        check_in_id_check_in
    ASC );

ALTER TABLE registro_arri ADD CONSTRAINT registro_arri_pk PRIMARY KEY ( id_registro_arri );

CREATE TABLE registro_pago (
    id_reg_pago              INTEGER NOT NULL,
    descripcion              VARCHAR2(75) NOT NULL,
    pago_total               INTEGER NOT NULL,
    reservas_id_reservas     INTEGER NOT NULL,
    metodo_pago_id_met_pago  INTEGER NOT NULL
);

CREATE INDEX registro_pago__idx ON
    registro_pago (
        metodo_pago_id_met_pago
    ASC );

CREATE INDEX registro_pago__idxv1 ON
    registro_pago (
        reservas_id_reservas
    ASC );

ALTER TABLE registro_pago ADD CONSTRAINT registro_pago_pk PRIMARY KEY ( id_reg_pago );

CREATE TABLE reservas (
    id_reservas                INTEGER NOT NULL,
    pago_reserva               INTEGER NOT NULL,
    num_acomp                  INTEGER,
    fecha_entrada              DATE NOT NULL,
    fecha_salida               DATE NOT NULL,
    multa                      INTEGER,
    subtotal                   INTEGER NOT NULL,
    cliente_rut                INTEGER NOT NULL,
    departamento_id_depto      INTEGER NOT NULL,
    metodo_pago_id_met_pago    INTEGER NOT NULL,
    std_reservas_id_std_resev  INTEGER NOT NULL
);

ALTER TABLE reservas ADD CONSTRAINT reservas_pk PRIMARY KEY ( id_reservas );

CREATE TABLE servicio_extra (
    id_servextra          INTEGER NOT NULL,
    tour                  CHAR(2),
    transporte            CHAR(2),
    precio                INTEGER,
    tour_id_tour          INTEGER NOT NULL,
    transporte_id_transp  INTEGER NOT NULL,
    reservas_id_reservas  INTEGER NOT NULL
);

CREATE INDEX servicio_extra__idx ON
    servicio_extra (
        tour_id_tour
    ASC );

CREATE INDEX servicio_extra__idxv1 ON
    servicio_extra (
        transporte_id_transp
    ASC );

ALTER TABLE servicio_extra ADD CONSTRAINT servicio_extra_pk PRIMARY KEY ( id_servextra );

CREATE TABLE std_depto (
    id_stdo_depto  INTEGER NOT NULL,
    descripcion    VARCHAR2(50) NOT NULL
);

ALTER TABLE std_depto ADD CONSTRAINT std_depto_pk PRIMARY KEY ( id_stdo_depto );

CREATE TABLE std_reservas (
    id_std_resev  INTEGER NOT NULL,
    descripcion   VARCHAR2(50) NOT NULL
);

ALTER TABLE std_reservas ADD CONSTRAINT std_reservas_pk PRIMARY KEY ( id_std_resev );

CREATE TABLE std_tour (
    id_std_tour  INTEGER NOT NULL,
    descripcion  VARCHAR2(50) NOT NULL
);

ALTER TABLE std_tour ADD CONSTRAINT std_tour_pk PRIMARY KEY ( id_std_tour );

CREATE TABLE std_transporte (
    id_std_transp  INTEGER NOT NULL,
    descripcion    VARCHAR2(50) NOT NULL
);

ALTER TABLE std_transporte ADD CONSTRAINT std_transporte_pk PRIMARY KEY ( id_std_transp );

CREATE TABLE tipo_personal (
    id_tipo_prs  INTEGER NOT NULL,
    descripcion  VARCHAR2(50) NOT NULL
);

ALTER TABLE tipo_personal ADD CONSTRAINT tipo_personal_pk PRIMARY KEY ( id_tipo_prs );

CREATE TABLE tour (
    id_tour               INTEGER NOT NULL,
    lugar                 VARCHAR2(75) NOT NULL,
    fecha                 DATE,
    std_tour_id_std_tour  INTEGER NOT NULL
);

ALTER TABLE tour ADD CONSTRAINT tour_pk PRIMARY KEY ( id_tour );

CREATE TABLE trans_condc (
    id_conduc           INTEGER NOT NULL,
    nombre_conc         VARCHAR2(50) NOT NULL,
    apellido_condc      VARCHAR2(50) NOT NULL,
    trans_vehi_id_vehi  INTEGER NOT NULL
);

CREATE INDEX trans_condc__idx ON
    trans_condc (
        trans_vehi_id_vehi
    ASC );

ALTER TABLE trans_condc ADD CONSTRAINT trans_condc_pk PRIMARY KEY ( id_conduc );

CREATE TABLE trans_vehi (
    id_vehi  INTEGER NOT NULL,
    modelo   VARCHAR2(50) NOT NULL,
    año      INTEGER NOT NULL
);

ALTER TABLE trans_vehi ADD CONSTRAINT trans_vehi_pk PRIMARY KEY ( id_vehi );

CREATE TABLE transporte (
    id_transp                     INTEGER NOT NULL,
    direccion                     VARCHAR2(75) NOT NULL,
    destino                       VARCHAR2(75) NOT NULL,
    zonas                         VARCHAR2(75) NOT NULL,
    comunas                       VARCHAR2(75) NOT NULL,
    fecha_trans                   DATE NOT NULL,
    std_transporte_id_std_transp  INTEGER NOT NULL,
    trans_condc_id_conduc         INTEGER NOT NULL
);

ALTER TABLE transporte ADD CONSTRAINT transporte_pk PRIMARY KEY ( id_transp );

CREATE TABLE zonas (
    id_zonas     INTEGER NOT NULL,
    descripcion  VARCHAR2(50) NOT NULL
);

ALTER TABLE zonas ADD CONSTRAINT zonas_pk PRIMARY KEY ( id_zonas );

ALTER TABLE acompañantes
    ADD CONSTRAINT acompañantes_reservas_fk FOREIGN KEY ( reservas_id_reservas )
        REFERENCES reservas ( id_reservas );

ALTER TABLE check_in
    ADD CONSTRAINT check_in_personal_fk FOREIGN KEY ( personal_id_personal )
        REFERENCES personal ( id_personal );

ALTER TABLE check_in
    ADD CONSTRAINT check_in_registro_pago_fk FOREIGN KEY ( registro_pago_id_reg_pago )
        REFERENCES registro_pago ( id_reg_pago );

ALTER TABLE check_out
    ADD CONSTRAINT check_out_personal_fk FOREIGN KEY ( personal_id_personal )
        REFERENCES personal ( id_personal );

ALTER TABLE check_out
    ADD CONSTRAINT check_out_registro_arri_fk FOREIGN KEY ( registro_arri_id_registro_arri )
        REFERENCES registro_arri ( id_registro_arri );

ALTER TABLE departamento
    ADD CONSTRAINT departamento_inventario_fk FOREIGN KEY ( inventario_id_inventario )
        REFERENCES inventario ( id_inventario );

ALTER TABLE departamento
    ADD CONSTRAINT departamento_std_depto_fk FOREIGN KEY ( std_depto_id_stdo_depto )
        REFERENCES std_depto ( id_stdo_depto );

ALTER TABLE departamento
    ADD CONSTRAINT departamento_zonas_fk FOREIGN KEY ( zonas_id_zonas )
        REFERENCES zonas ( id_zonas );

ALTER TABLE personal
    ADD CONSTRAINT personal_tipo_personal_fk FOREIGN KEY ( tipo_personal_id_tipo_prs )
        REFERENCES tipo_personal ( id_tipo_prs );

ALTER TABLE personal
    ADD CONSTRAINT personal_zonas_fk FOREIGN KEY ( zonas_id_zonas )
        REFERENCES zonas ( id_zonas );

ALTER TABLE registro_arri
    ADD CONSTRAINT registro_arri_check_in_fk FOREIGN KEY ( check_in_id_check_in )
        REFERENCES check_in ( id_check_in );

ALTER TABLE registro_pago
    ADD CONSTRAINT registro_pago_metodo_pago_fk FOREIGN KEY ( metodo_pago_id_met_pago )
        REFERENCES metodo_pago ( id_met_pago );

ALTER TABLE registro_pago
    ADD CONSTRAINT registro_pago_reservas_fk FOREIGN KEY ( reservas_id_reservas )
        REFERENCES reservas ( id_reservas );

ALTER TABLE reservas
    ADD CONSTRAINT reservas_cliente_fk FOREIGN KEY ( cliente_rut )
        REFERENCES cliente ( rut );

ALTER TABLE reservas
    ADD CONSTRAINT reservas_departamento_fk FOREIGN KEY ( departamento_id_depto )
        REFERENCES departamento ( id_depto );

ALTER TABLE reservas
    ADD CONSTRAINT reservas_metodo_pago_fk FOREIGN KEY ( metodo_pago_id_met_pago )
        REFERENCES metodo_pago ( id_met_pago );

ALTER TABLE reservas
    ADD CONSTRAINT reservas_std_reservas_fk FOREIGN KEY ( std_reservas_id_std_resev )
        REFERENCES std_reservas ( id_std_resev );

ALTER TABLE servicio_extra
    ADD CONSTRAINT servicio_extra_reservas_fk FOREIGN KEY ( reservas_id_reservas )
        REFERENCES reservas ( id_reservas );

ALTER TABLE servicio_extra
    ADD CONSTRAINT servicio_extra_tour_fk FOREIGN KEY ( tour_id_tour )
        REFERENCES tour ( id_tour );

ALTER TABLE servicio_extra
    ADD CONSTRAINT servicio_extra_transporte_fk FOREIGN KEY ( transporte_id_transp )
        REFERENCES transporte ( id_transp );

ALTER TABLE tour
    ADD CONSTRAINT tour_std_tour_fk FOREIGN KEY ( std_tour_id_std_tour )
        REFERENCES std_tour ( id_std_tour );

ALTER TABLE trans_condc
    ADD CONSTRAINT trans_condc_trans_vehi_fk FOREIGN KEY ( trans_vehi_id_vehi )
        REFERENCES trans_vehi ( id_vehi );

ALTER TABLE transporte
    ADD CONSTRAINT transporte_std_transporte_fk FOREIGN KEY ( std_transporte_id_std_transp )
        REFERENCES std_transporte ( id_std_transp );

ALTER TABLE transporte
    ADD CONSTRAINT transporte_trans_condc_fk FOREIGN KEY ( trans_condc_id_conduc )
        REFERENCES trans_condc ( id_conduc );

