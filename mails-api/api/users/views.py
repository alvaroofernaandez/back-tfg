from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import User
from django.core.mail import send_mail
from .UserSerializer import UserSerializer
from .utils import send_email_users_where_allowed

class SendSingleEmailAPIView(APIView):
    def post(self, request):
        """
        Endpoint para enviar un correo personalizado a un usuario específico.
        """
        # Recibir los datos desde el cuerpo de la solicitud.
        correo = request.data.get("correo")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        # Validar que todos los campos sean proporcionados
        if not correo or not asunto or not mensaje:
            return Response(
                {"error": "Por favor, proporciona correo, asunto y mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar que el usuario con el correo proporcionado existe en la base de datos.
            if not User.objects.filter(email=correo).exists():
                return Response(
                    {"error": f"No existe un usuario registrado con el correo: {correo}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Enviar el correo
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="jdeomoya@gmail.com",  # Aquí va el correo que enviará los mensajes.
                recipient_list=[correo],
                fail_silently=False,
            )

            return Response({"message": "Correo enviado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class SendEmailsAPIView(APIView):
    def post(self, request):
        try:
            send_email_users_where_allowed()  # Llama a la función para enviar correos
            return Response({"message": "Correos enviados exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'])
    def send_personalized_email(self, request):
        """
        Endpoint para enviar un correo personalizado a un usuario con un asunto y un mensaje.
        """
        # Recibir los datos desde el cuerpo de la solicitud.
        correo = request.data.get("correo")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        # Validar que todos los campos sean proporcionados
        if not correo or not asunto or not mensaje:
            return Response(
                {"error": "Por favor, proporciona correo, asunto y mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar que el usuario con el correo proporcionado existe en la base de datos.
            if not User.objects.filter(email=correo).exists():
                return Response(
                    {"error": f"No existe un usuario registrado con el correo: {correo}"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Enviar el correo
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="jdeomoya@gmail.com",  # Aquí va el correo que enviará los mensajes.
                recipient_list=[correo],
                fail_silently=False,
            )

            return Response({"message": "Correo enviado exitosamente!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @action(detail=False, methods=['POST'])
    def send_personalized_email_many_users(self, request):
        usuarios = request.data.get("usuarios")
        asunto = request.data.get("asunto")
        mensaje = request.data.get("mensaje")

        if not usuarios or not isinstance(usuarios,list) or not asunto or not mensaje:
            return Response(
                {"error": "Debes proporcionar una lista de usuarios, un asunto y un mensaje."},
                status=status.HTTP_400_BAD_REQUEST
            )

        correos_validos = []
        correos_no_encontrado = []

        for correo in usuarios:
            if User.objects.filter(email=correo).exists():
                correos_validos.append(correo)
            else:
                correos_no_encontrado.append(correo)

        if not correos_validos:
            return Response(
                {"error": "Ninguno de los correos proporcionados existe en la base de datos."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Enviar el correo a los usuarios encontrados
        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email="jdeomoya@gmail.com",
                recipient_list=correos_validos,
                fail_silently=False,
            )
            respuesta = {
                "mensaje": "Correos enviados exitosamente.",
                "correos_enviados": correos_validos,
            }
            if correos_no_encontrado:
                respuesta["correos_no_encontrados"] = correos_no_encontrado

            return Response(respuesta, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al enviar correos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserCreateAPIView(APIView):
    def getUserById(self,request):
        id_alumno = request.query_params.get('id')

        if not id_alumno:
            return Response({"error": "id_alumno es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=id_alumno).first

        serializer = UserSerializer(user,many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Usuario creado exitosamente!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)