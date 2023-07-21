from django.shortcuts import render
import openai
import requests

from .forms import AnswerForm


openai.api_key = "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"


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
{"role": "user", "content": f"""Use template and new info. If given in Korean, leave it in Korean. If time is not included in the info, just write the date.
Template:
@mkt-kr
[PROMOUPDATE] - [merchant name(brand) goes here]
[Short promo summary go here.] - (M/D HH:mm AM/PM - M/D HH:mm AM/PM Convert to Korea time if not in KST)
  ●   [Long promo summarized without date information go here, divide each sentence by   ●   ]
  ●   Promocode: [promocode go here, remove this line if not given or mentioned elsewhere]
  ●   Link: [Link goes here,remove this line if not given]
T&C:
[Other restrictions go here, remove line if not given & divided each sentence with -]
CC: @[either Minji, Hannah, or Mike]
https://docs.google.com/spreadsheets/d/10KWNDZlnMv6lTCqa0COnOuTgzeTA2D5h0QXhAj5TzGA/edit#gid=2102863397

If there are multiple info, divide by number under [PROMPUPDATE]. Refer to the example here:
@mkt-kr
[PROMOUPDATE] - MR PORTER
1. MR PORTER x HSBC 2023 - (7/14 - 9/1)
  ●   15% discount on all orders for HSBC customers.
  ●   Applicable to both full price and markdown items.
  ●   Only available for shipping to APAC countries.
  ●   Promocode: HSBC15
T&C:
*Exclusions apply
2. MR PORTER x VISA 2023 - (7/31 3:00 PM - 8/31 2:59 PM)
  ●   Enjoy a 15% discount on all your orders at MR PORTER
  ●   Valid for both full price and markdown items.
  ●   Promocode: SHINHAN15 for Shinhan bank customers
        WOORI15 for Woori bank customers
        HYUNDAI15 for Hyundai bank customers
T&C:
- Offer valid for South Korea customers only
- Brand exclusion list: Same list as above
CC: 
@Hannah Jung
https://docs.google.com/spreadsheets/d/10KWNDZlnMv6lTCqa0COnOuTgzeTA2D5h0QXhAj5TzGA/edit#gid=2102863397 

Also write this so I can paste into excel. Ensure you remove time if not given:


M/D/2023 HH:mm AM/PM	M/D/2023 HH:mm AM/PM	[promocode go here, leave empty if not given]	[Short promo, Long promo, and T&C from above go here, replace   ●   with -]	[Link goes here, remove if not given]

Again, if there're multiple info, use multiple rows following this example:
7/14/2023 11:00 AM	9/1/2023 3:30 AM	HSBC15	"MR PORTER x HSBC 2023
- 15% discount on all orders for HSBC customers.
- Applicable to both full price and markdown items.
- Only available for shipping to APAC countries."
7/31/2023 3:00 PM	8/31/2023 2:59 PM	SHINHAN15, WOORI15, HYUNDAI15	"MR PORTER x VISA 2023
- Enjoy a 15% discount on all your orders at MR PORTER
- Valid for both full price and markdown items.
- Promocode: SHINHAN15 for Shinhan bank customers
        WOORI15 for Woori bank customers
        HYUNDAI15 for Hyundai bank customers
T&C:
- Offer valid for South Korea customers only
- Brand exclusion list: Same list as above"

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

    return render(request, "kist.html", {"form": form})