from django_filters import rest_framework as filters
from .models import Historicos, Sensores

class HistoricoFilter(filters.FilterSet):
    # Filtro por intervalo de data (Critério 15: data)
    data_inicio = filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    data_fim = filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    
    # Filtro por valor (ex: buscar apenas temperaturas acima de 30°C)
    valor_min = filters.NumberFilter(field_name="valor", lookup_expr='gte')
    
    class Meta:
        model = Historicos
        fields = ['sensor', 'sensor__mic__ambiente__local'] # Filtro por sensor e local

class SensorFilter(filters.FilterSet):
    class Meta:
        model = Sensores
        fields = ['sensor', 'status', 'mic__ambiente__local'] # Filtro por tipo, status e local