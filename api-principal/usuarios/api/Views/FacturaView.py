from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from weasyprint import HTML

from ..Models.CitaModel import Cita
from ..Models.FacturaModel import Factura
from ..Serializers.FacturaSerializer import FacturaSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

    @action(detail=False, methods=['get'], renderer_classes=[TemplateHTMLRenderer, JSONRenderer])
    def detalle(self, request):
        id = request.query_params.get('id')
        download = request.query_params.get('download') == '1'

        if not id:
            raise ValidationError("Se debe proporcionar un id.")

        factura = get_object_or_404(Factura, pk=id)
        factura_data = FacturaSerializer(factura).data

        if download:
            html_content = render_to_string('factura/factura.html', {'factura': factura_data})
            pdf_file = HTML(string=html_content).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=factura_{id}.pdf'
            return response

        if request.accepted_renderer.format == 'html':
            return Response({'factura': factura_data}, template_name='factura/factura.html')
        else:
            return Response({'factura': factura_data})

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        factura = serializer.save()

        cita = factura.cita
        if cita.estado != 'completada':
            cita.estado = 'completada'
            cita.save()

        return Response({'factura': FacturaSerializer(factura).data}, status=status.HTTP_201_CREATED)
