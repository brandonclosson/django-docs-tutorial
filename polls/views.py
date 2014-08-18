from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic

from polls.models import Poll, Choice

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# def index(request):
# 	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
# 	context = {'latest_poll_list': latest_poll_list}
# 	return render(request, 'polls/index.html', context)

	
	#long form of index view
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#	'latest_poll_list': latest_poll_list,
	#})
	#return HttpResponse(template.render(context))

# def detail(request, poll_id):
# 	poll = get_object_or_404(Poll, pk=poll_id)
	#long form of detail view
	#try:
	#	poll = Poll.objects.get(pk=poll_id)
	#except Poll.DoesNotExist:
	#	raise Http404
# 	context = {'poll': poll}
# 	return render(request, 'polls/detail.html', context)

# def results(request, poll_id):
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	return render(request, 'polls/results.html', {'poll': poll})
