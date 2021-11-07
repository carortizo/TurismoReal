# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acompañantes(models.Model):
    rut = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=75)
    reservas_id_reservas = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='reservas_id_reservas')

    def __str__(self):
        return self.rut

    class Meta:
        managed = False
        db_table = 'acompañantes'


class CheckIn(models.Model):
    id_check_in = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=75)
    registro_pago_id_reg_pago = models.ForeignKey('RegistroPago', models.DO_NOTHING, db_column='registro_pago_id_reg_pago')
    personal_id_personal = models.ForeignKey('Personal', models.DO_NOTHING, db_column='personal_id_personal')

    def __str__(self):
        return self.descripcion
    class Meta:
        managed = False
        db_table = 'check_in'


class CheckOut(models.Model):
    id_check_out = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=75)
    multa = models.BigIntegerField()
    registro_arri_id_registro_arri = models.ForeignKey('RegistroArri', models.DO_NOTHING, db_column='registro_arri_id_registro_arri')
    personal_id_personal = models.ForeignKey('Personal', models.DO_NOTHING, db_column='personal_id_personal')

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'check_out'


class Cliente(models.Model):
    rut = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=75)
    apellidos = models.CharField(max_length=75)
    telefono = models.BigIntegerField()
    correo = models.EmailField(verbose_name="email", max_length=60,unique=True)
    contraseña = models.CharField(max_length=75)

    def __str__(self):
        return self.rut

    class Meta:
        managed = False
        db_table = 'cliente'


class Departamento(models.Model):
    id_depto = models.IntegerField(primary_key=True)
    metros_cua = models.BigIntegerField()
    direccion = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=75)
    precio = models.BigIntegerField()
    img = models.BinaryField(blank=True, null=True)
    zonas_id_zonas = models.ForeignKey('Zonas', models.DO_NOTHING, db_column='zonas_id_zonas')
    inventario_id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='inventario_id_inventario')
    std_depto_id_stdo_depto = models.ForeignKey('StdDepto', models.DO_NOTHING, db_column='std_depto_id_stdo_depto')

    def __str__(self):
        return self.direccion
    
    class Meta:
        managed = False
        db_table = 'departamento'


class Inventario(models.Model):
    id_inventario = models.IntegerField(primary_key=True)
    habitacion = models.BigIntegerField()
    camas = models.CharField(max_length=75)
    incluido = models.CharField(max_length=255)
    baños = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'inventario'


class MetodoPago(models.Model):
    id_met_pago = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'metodo_pago'


class Personal(models.Model):
    id_personal = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=75)
    apellidos = models.CharField(max_length=75)
    rut = models.BigIntegerField()
    telefono = models.BigIntegerField()
    correo = models.CharField(max_length=75)
    contraseña = models.CharField(max_length=75)
    tipo_personal_id_tipo_prs = models.ForeignKey('TipoPersonal', models.DO_NOTHING, db_column='tipo_personal_id_tipo_prs')
    zonas_id_zonas = models.ForeignKey('Zonas', models.DO_NOTHING, db_column='zonas_id_zonas')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'personal'


class RegistroArri(models.Model):
    id_registro_arri = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=75)
    pago_total = models.CharField(max_length=75)
    check_in_id_check_in = models.ForeignKey(CheckIn, models.DO_NOTHING, db_column='check_in_id_check_in')

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'registro_arri'


class RegistroPago(models.Model):
    id_reg_pago = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=75)
    pago_total = models.BigIntegerField()
    reservas_id_reservas = models.ForeignKey('Reservas', models.DO_NOTHING, db_column='reservas_id_reservas')
    metodo_pago_id_met_pago = models.ForeignKey(MetodoPago, models.DO_NOTHING, db_column='metodo_pago_id_met_pago')
    
    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'registro_pago'


class Reservas(models.Model):
    id_reservas = models.IntegerField(primary_key=True)
    pago_reserva = models.BigIntegerField()
    num_acomp = models.BigIntegerField(blank=True, null=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    multa = models.BigIntegerField(blank=True, null=True)
    subtotal = models.BigIntegerField()
    cliente_rut = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_rut')
    departamento_id_depto = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='departamento_id_depto')
    metodo_pago_id_met_pago = models.ForeignKey(MetodoPago, models.DO_NOTHING, db_column='metodo_pago_id_met_pago')
    std_reservas_id_std_resev = models.ForeignKey('StdReservas', models.DO_NOTHING, db_column='std_reservas_id_std_resev')



    class Meta:
        managed = False
        db_table = 'reservas'


class ServicioExtra(models.Model):
    id_servextra = models.IntegerField(primary_key=True)
    tour = models.CharField(max_length=2, blank=True, null=True)
    transporte = models.CharField(max_length=2, blank=True, null=True)
    precio = models.BigIntegerField(blank=True, null=True)
    tour_id_tour = models.ForeignKey('Tour', models.DO_NOTHING, db_column='tour_id_tour')
    transporte_id_transp = models.ForeignKey('Transporte', models.DO_NOTHING, db_column='transporte_id_transp')
    reservas_id_reservas = models.ForeignKey(Reservas, models.DO_NOTHING, db_column='reservas_id_reservas')


    class Meta:
        managed = False
        db_table = 'servicio_extra'


class StdDepto(models.Model):
    id_stdo_depto = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'std_depto'


class StdReservas(models.Model):
    id_std_resev = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'std_reservas'


class StdTour(models.Model):
    id_std_tour = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'std_tour'


class StdTransporte(models.Model):
    id_std_transp = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'std_transporte'


class TipoPersonal(models.Model):
    id_tipo_prs = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'tipo_personal'


class Tour(models.Model):
    id_tour = models.IntegerField(primary_key=True)
    lugar = models.CharField(max_length=75)
    fecha = models.DateField(blank=True, null=True)
    std_tour_id_std_tour = models.ForeignKey(StdTour, models.DO_NOTHING, db_column='std_tour_id_std_tour')

    def __str__(self):
        return self.lugar

    class Meta:
        managed = False
        db_table = 'tour'


class TransCondc(models.Model):
    id_conduc = models.IntegerField(primary_key=True)
    nombre_conc = models.CharField(max_length=50)
    apellido_condc = models.CharField(max_length=50)
    trans_vehi_id_vehi = models.ForeignKey('TransVehi', models.DO_NOTHING, db_column='trans_vehi_id_vehi')

    def __str__(self):
        return self.nombre_conc

    class Meta:
        managed = False
        db_table = 'trans_condc'


class TransVehi(models.Model):
    id_vehi = models.IntegerField(primary_key=True)
    modelo = models.CharField(max_length=50)
    año = models.BigIntegerField()

    def __str__(self):
        return self.modelo

    class Meta:
        managed = False
        db_table = 'trans_vehi'


class Transporte(models.Model):
    id_transp = models.IntegerField(primary_key=True)
    direccion = models.CharField(max_length=75)
    destino = models.CharField(max_length=75)
    zonas = models.CharField(max_length=75)
    comunas = models.CharField(max_length=75)
    fecha_trans = models.DateField()
    std_transporte_id_std_transp = models.ForeignKey(StdTransporte, models.DO_NOTHING, db_column='std_transporte_id_std_transp')
    trans_condc_id_conduc = models.ForeignKey(TransCondc, models.DO_NOTHING, db_column='trans_condc_id_conduc')

    def __str__(self):
        return self.destino

    class Meta:
        managed = False
        db_table = 'transporte'


class Zonas(models.Model):
    id_zonas = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = False
        db_table = 'zonas'
