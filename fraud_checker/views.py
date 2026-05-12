from django.shortcuts import render
from .services import FraudModelService

def home(request):
    result = None
    formatted_probability = None
    
    if request.method == 'POST':
        # Get data from the HTML form
        try:
            data = {
                'Avg min between sent tnx': float(request.POST.get('avg_min', 0)),
                'Sent tnx': int(request.POST.get('sent_tnx', 0)),
                'Received Tnx': int(request.POST.get('received_tnx', 0)),
                'total Ether sent': float(request.POST.get('total_eth', 0)),
            }
            
            # Call our Service
            result, probability = FraudModelService.predict(data)
            
            # Format probability only if prediction was successful
            if probability is not None:
                formatted_probability = f"{probability * 100:.1f}%"
                
        except Exception as e:
            result = f"Error: {e}"

    return render(request, 'fraud_checker/home.html', {
        'result': result, 
        'probability': formatted_probability
    })




# Create your views here.
