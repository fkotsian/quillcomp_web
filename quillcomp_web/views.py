from django.http import HttpResponse
from django.template import loader
from .models import Prompt, StudentResponse

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
    return HttpResponse("Abc123")
