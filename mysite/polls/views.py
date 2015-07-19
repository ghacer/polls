from django.shortcuts import render,get_object_or_404
from models import Question,Choice
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
	return Question.objects.filter(
		pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
	return Question.objects.filter(pub_date__lte=timezone.now())

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
	return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, pk):
    p = get_object_or_404(Question, pk=pk)
    try:
	selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KEyError, Choice.DoseNotExist):
	return render(request, 'polls/detail.html', {
		'question': p,
		'error_message': "You didn't select a choice.",
	})
    else:
	selected_choice.votes += 1
	selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
# Create your views here.
