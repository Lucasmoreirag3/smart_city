from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action # Para criar rotas extras
from django.utils import timezone
from datetime import timedelta
import pandas as pd
from .models import Sensores, Historicos, Ambientes, Locais, Responsaveis, Microcontroladores
from .serializers import * # Importa todos os seus serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filters import HistoricoFilter, SensorFilter

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensorFilter

    @action(detail=False, methods=['post'])
    def importar_planilha(self, request):
        arquivo = request.FILES.get('arquivo')
        if not arquivo:
            return Response({"error": "Arquivo não enviado"}, status=400)
        
        df = pd.read_excel(arquivo)
        for _, row in df.iterrows():
           
            local_obj, _ = Locais.objects.get_or_create(local=row['Local'])
            # Adicione os outros campos conforme a estrutura da sua planilha
        return Response({"message": "Importação concluída!"})

class HistoricosViewSet(viewsets.ModelViewSet):
    queryset = Historicos.objects.all()
    serializer_class = HistoricosSerializer
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    def create(self, request, *args, **kwargs):
        sensor_id = request.data.get('sensor')
        sensor = Sensores.objects.get(id=sensor_id)
        
       
        if not sensor.status:
            return Response(
                {"error": "Não é possível registrar medições. Sensor inativo."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def ultimas_24h(self, request):
        sensor_id = request.query_params.get('sensor')
        if not sensor_id:
            return Response({"error": "Parâmetro 'sensor' é obrigatório"}, status=400)
        
        try:
            sensor = Sensores.objects.get(id=sensor_id)
        except Sensores.DoesNotExist:
            return Response({"error": "Sensor não encontrado"}, status=404)
        
        agora = timezone.now()
        ontem = agora - timedelta(hours=24)
        historicos = Historicos.objects.filter(sensor=sensor, timestamp__gte=ontem)
        serializer = self.get_serializer(historicos, many=True)
        return Response(serializer.data)
    
class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResponsaveisViewSet(viewsets.ModelViewSet):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer
    permission_classes = [permissions.IsAuthenticated]

class AmbientesViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [permissions.IsAuthenticated]

class MicrocontroladoresViewSet(viewsets.ModelViewSet):
    queryset = Microcontroladores.objects.all()
    serializer_class = MicrocontroladoresSerializer
    permission_classes = [permissions.IsAuthenticated]

    