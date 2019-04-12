from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.conf import settings
from .models import Prompt, StudentResponse
from .nlp import Nlp

# Create your views here.
def landing(request):
    return HttpResponse("Hello, world! The Quill Comp app is live!")

def prompts(request):
    prompts = Prompt.objects.all()[:5]
    context = {
        'prompts': prompts,
    }
    template = loader.get_template('quillcomp_web/prompts/index.html')
    return HttpResponse(template.render(context, request))

def student_responses(request, prompt_id):
    responses = StudentResponse.objects.filter(prompt_id = prompt_id)
    prompt = Prompt.objects.get(id = prompt_id)
    context = {
        'prompt': prompt,
        'responses': responses,
    }
    template = loader.get_template('quillcomp_web/student_responses/index.html')
    return HttpResponse(template.render(context, request))

def new_response(request, prompt_id):
    prompt = Prompt.objects.get(id = prompt_id)

    if request.method == 'POST':
        print("POSTDATA")
        print(request.POST)
        user_response = request.POST.get('response_text', None)
    else:
        user_response = " they should offer a healthy option so that kids can have a snack if they get hungry."

    print("USER RESPONSE:")
    print(user_response)

    # run NLP code
    nlp = Nlp(prompt = prompt.text, training_sents = settings.STUDENT_RESPONSES_BUT)
    user_sent = prompt.text + " " + user_response

    print(user_sent)

    feedback_codes = nlp.feedback_for_sent(user_sent)

    feedback = nlp.translated_feedback(feedback_codes)

    print("FEEDBACK CODES!")
    print(feedback_codes)
    print(feedback)

    # respond JSON
    response_data = {
        'feedback': feedback,
    }
    return JsonResponse(response_data)

