from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import AuthForm, VariableForm
import re
import boto3
import io


dict = {}
def rec(fileIndex, phraseCount, offset):
    client = boto3.client('s3')
    bytes_buffer = io.BytesIO()
    client.download_fileobj(Bucket="tbbucketstudyinformation", Key=str(fileIndex) + ".txt", Fileobj=bytes_buffer)
    byte_value = bytes_buffer.getvalue()
    document = byte_value.decode()

    del byte_value
    del bytes_buffer
    del client

    countedInFile = {}

    if phraseCount != 0 and phraseCount != 1:
        if offset > 0:
            for i in range(offset):
                document = document[(document.find(" ") + 1):]
        phrases = re.findall(" ".join(["[^\s]+"] * phraseCount), document)
        for phrase in phrases:
            phrase = re.sub(r'[^\w\s]','',phrase).lower().strip()
            if phrase != "":
                dict[phrase] = (dict[phrase][0] + 1, (dict[phrase][1] + 1 if not phrase in countedInFile else dict[phrase][1])) if phrase in dict else (1, 1)
                countedInFile[phrase] = True
    elif phraseCount == 0 or phraseCount == 1:
        for word in document.split():
            word = re.sub(r'[^\w\s]','',word).lower()
            if word != "":
                dict[word] = (dict[word][0] + 1, (dict[word][1] + 1 if not word in countedInFile else dict[word][1])) if word in dict else (1, 1)
                countedInFile[word] = True

    del countedInFile
    del document

    if fileIndex == 82:
        return
    rec(fileIndex + 1, phraseCount, offset)

def index(request):
    if request.method != "POST":
        return HttpResponse("You are not authorized. Git on now! (1)")
    form = AuthForm(request.POST)
    if not form.is_valid() or (not "pw" in form.cleaned_data):
        return HttpResponse("You are not authorized. Git on now! (2)")

    pw = form.cleaned_data["pw"]
    if pw != "uiabfe92qheb1s9b21qk87s":
        return HttpResponse("Incorrect Password")

    return HttpResponse(loader.get_template('studytokenizer/index.html').render({"form": VariableForm()}, request))


def download(request):
    global dict
    if request.method != "POST":
        return HttpResponse("You are not authorized. Git on now! (3)")
    form = VariableForm(request.POST)
    if not form.is_valid() or (not "lines" in form.cleaned_data):
        return HttpResponse("You are not authorized. Git on now! (4)")

    lines = form.cleaned_data["lines"]
    phraseCount = 0
    if "phrases" in form.cleaned_data:
        phraseCount = form.cleaned_data["phrases"]

    offset = 0
    if "offset" in form.cleaned_data:
        offset = form.cleaned_data["offset"]

    sortKey = 1
    if "sortKey" in form.cleaned_data:
        sortKey = form.cleaned_data["sortKey"]

    client = boto3.client('s3')
    bytes_buffer = io.BytesIO()
    client.download_fileobj(Bucket="tbbucketstudyinformation", Key="0.txt", Fileobj=bytes_buffer)
    byte_value = bytes_buffer.getvalue()
    document = byte_value.decode()

    del byte_value
    del bytes_buffer
    del client

    countedInFile = {}

    if phraseCount != 0 and phraseCount != 1:
        if offset > 0:
            for i in range(offset):
                document = document[(document.find(" ") + 1):]
        phrases = re.findall(" ".join(["[^\s]+"] * phraseCount), document)
        for phrase in phrases:
            phrase = re.sub(r'[^\w\s]','',phrase).lower().strip()
            if phrase != "":
                dict[phrase] = (dict[phrase][0] + 1, (dict[phrase][1] + 1 if not phrase in countedInFile else dict[phrase][1])) if phrase in dict else (1, 1)
                countedInFile[phrase] = True

    elif phraseCount == 0 or phraseCount == 1:
        for word in document.split():
            word = re.sub(r'[^\w\s]','',word).lower()
            if word != "":
                dict[word] = (dict[word][0] + 1, (dict[word][1] + 1 if not word in countedInFile else dict[word][1])) if word in dict else (1, 1)
                countedInFile[word] = True

    del countedInFile


    rec(1, phraseCount, offset)

    returnString = ""
    sortedDict = {k: v for k, v in sorted(dict.items(), key=lambda item: (item[1][1] if sortKey == 1 else item[1][0]))}
    keys = list(sortedDict)
    dictLength = len(sortedDict)
    for i in range(dictLength):
        key = keys[dictLength - 1 - i]
        occurrences = sortedDict[key][0]
        appearances = sortedDict[key][1]
        returnString = returnString + str("Term: \"" + str(key) + "\" ----- Number of occurrences: " + str(occurrences) + " ----- Number of file appearances: " + str(appearances) + "\n")
        if i > lines:
            break

    response = HttpResponse(returnString, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format("filename.txt")
    dict.clear()
    return response
