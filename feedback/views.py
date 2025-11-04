from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Story, Feedback
from .forms import FeedbackForm

def story_list(request):
    stories = Story.objects.select_related('outlet').annotate(feedback_count=Count('feedbacks')).all()
    return render(request, 'feedback/story_list.html', {'stories': stories})

def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    feedbacks = story.feedbacks.select_related('region', 'user')[:200]

    # aggregate averages for the story
    agg = story.feedbacks.aggregate(
        avg_accuracy=Avg('accuracy'),
        avg_bias=Avg('bias'),
        avg_clarity=Avg('clarity'),
        avg_relevance=Avg('relevance'),
        count=Count('id')
    )

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.story = story
            if request.user.is_authenticated:
                fb.user = request.user
            fb.save()
            return redirect('feedback:submit_thanks')
    else:
        form = FeedbackForm()

    context = {
        'story': story,
        'feedbacks': feedbacks,
        'agg': agg,
        'form': form,
    }
    return render(request, 'feedback/story_detail.html', context)

def submit_thanks(request):
    return render(request, 'feedback/submit_thanks.html')

# Optional: staff view to create stories via web (otherwise use admin)
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from .models import Story

class StoryCreateForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title','slug','published_date','outlet','url','excerpt']

@staff_member_required
def story_create(request):
    if request.method == 'POST':
        form = StoryCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback:story_list')
    else:
        form = StoryCreateForm()
    return render(request, 'feedback/story_form.html', {'form': form})