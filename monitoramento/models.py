from django.db import models

class Usuarios(models.Model):
    TIPO_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Usuario', 'Usuário'),
    ]
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome

class Locais(models.Model):
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.local

class Responsaveis(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Ambientes(models.Model):
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    responsavel = models.ForeignKey(Responsaveis, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.local} - {self.descricao}"

class Microcontroladores(models.Model):
    modelo = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField(default=True)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)

    def __str__(self):
        return self.modelo

class Sensores(models.Model):
    TIPO_SENSOR_CHOICES = [
        ('temperatura', 'Temperatura'),
        ('umidade', 'Umidade'),
        ('luminosidade', 'Luminosidade'),
        ('contador', 'Contador'),
    ]
    UNIDADE_CHOICES = [
        ('°C', '°C'),
        ('%', '%'),
        ('lux', 'lux'),
        ('uni', 'uni'),
    ]
    
    sensor = models.CharField(max_length=50, choices=TIPO_SENSOR_CHOICES)
    unidade_med = models.CharField(max_length=10, choices=UNIDADE_CHOICES)
    mic = models.ForeignKey(Microcontroladores, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sensor} ({self.mic.modelo})"

class Historicos(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    valor = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.sensor}: {self.valor} em {self.timestamp}"