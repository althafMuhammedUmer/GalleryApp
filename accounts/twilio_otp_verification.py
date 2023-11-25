from decouple import config
from twilio.rest import Client
from django.http import JsonResponse


def generate_twilio_otp(request):

    if request.method == "POST":
        user_contact = request.POST.get('user_contact')
        number = '+971' + str(user_contact)
  
        TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
        TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
        TWILIO_SERVICE_SID = config('TWILIO_SERVICE_SID')

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        verification = client.verify \
                            .services(TWILIO_SERVICE_SID) \
                            .verifications \
                            .create(to=number, channel='sms')
        
        print(verification.sid)

        return JsonResponse({'otp send': True})
        
        
        
    return JsonResponse({'error': "Invalid request."})