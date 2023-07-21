from django.shortcuts import render
import openai
import requests

from .forms import AnswerForm


openai.api_key = ""


# AI message generator
def generate_message(request, prompt):
    response = openai.ChatCompletion.create(
    model="gpt-4",
    temperature=0,
    max_tokens=4000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    # 여기에서 챗봇을 커스텀하세요
    messages=[
{"role": "user", "content": f"""Use example and new info. Info is in this order: start date, end date, CPA(%) and additional description if any, CB(%) and additional description if any, name of package(ex: Platinum), campaign name if any. If the end time is exactly 12:00 PM, change it into 11:59 AM on the same date. If the given end time is exactly 12:00 AM, substract a day and put 11:59 PM instead. 

Example:

5 Jul 12:00 AM	12 Jul 11:59 PM	13%	11%	Gold	777 Lucky Sales

New info:
{prompt}"""}
]
    )
    generated_message = response['choices'][0]['message']['content']
    print(generated_message)
    return generated_message

# Main page
def index(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        # if form.is_valid():
        question= form['prompt'].value()
        message = generate_message(request, form['prompt'].value().strip())
        context = {
          'question': question,
          'message': message,
        }
        return render(request, 'answer.html', context)
    else:
        form = AnswerForm()

    return render(request, "upsize.html", {"form": form})